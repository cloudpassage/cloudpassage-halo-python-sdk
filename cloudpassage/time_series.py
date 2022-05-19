import operator
import time
from .http_helper import HttpHelper
from multiprocessing.dummy import Pool as ThreadPool
from .exceptions import CloudPassageValidation
# urllib in py 2 vs 3 is quite different...
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class TimeSeries(object):
    """Wrap time-series object retrieval in a generator.

    This method enables the consumption of time-ordered API objects as a
    generator. This method is multi-threaded and ensures that objects are
    yielded in chronological order according to the ``created_at`` field.
    This method also automatically adjusts the number of threads in use
    based on the volume of objects published via the selected API endpoint.

    In order to cleanly stop the generator, set the object's ``stop``
    attribute to ``True``.

    Example::

        # Print event IDs as they occur
        import datetime
        import os
        import cloudpassage
        start_time = datetime.datetime.now().isoformat()
        key = os.getenv("HALO_API_KEY")
        secret = os.getenv("HALO_API_SECRET_KEY")
        session = cloudpassage.HaloSession(key, secret)
        event_stream = cloudpassage.TimeSeries(session, start_time,
                                               "/v1/events", "events")
        for x in event_stream:
            print(x["id"])

    Args:
        session(object): HaloSession object.
        start_time(str): ISO 8601-formatted timestamp.
        start_url(str): Path from URL, no hostname and no URL-encoded params.
        item_key(str): Top-level key, below which is a list of target items.
        params(dict): Parameters for URL, which will be URL-encoded.

    Attributes:
        stop(bool):
            Set to ``False`` by default. When set to ``True``, the generator
            will return, effecting a clean exit.
    """

    allowed_urls = ["/v1/events", "/v1/scans", "/v3/issues"]

    def __init__(self, session, start_time, start_url, item_key, params={}):
        self.url = start_url
        self.params = params
        self.start_url = start_url
        self.batch_size = 1
        self.page_size = 50
        self.session = session
        self.max_threads = 10
        self.item_key = item_key
        self.sort_key = "created_at"
        self.last_item_id = None
        self.params["since"] = start_time
        self.params["per_page"] = self.page_size
        self.params["sort_by"] = "created_at.asc"
        self.verify_start_url(start_url)
        self.stop = False
        self.prior_batch_ids = set([])
        return

    def __iter__(self):
        """Yields one item from a time-series query against Halo. Forever."""
        while True:
            if self.stop:
                return
            for item in self.get_next_batch():
                yield item

    def adjust_batch_size(self, adjustment_factor):
        """Adjust the batch size for subsequent queries against Halo API.

        We will never take the batch size below 1 or over the original maximum
        thread count.

        Args:
            adjustent_factor(int): Number, positive or negative, by which we
                should increase or decrease the number of concurrent requsts
                agains the Halo API.
        """
        target_batch_size = adjustment_factor + self.batch_size
        if target_batch_size < 1:  # Don't go below one page.
            self.batch_size = 1
        elif target_batch_size > self.max_threads:  # Don't exceed max_threads.
            self.batch_size = self.max_threads
        else:
            self.batch_size = target_batch_size
        return

    @classmethod
    def create_url_batch(cls, path, batch_size, params={}):
        """Create a batch of URLs for pulling time-series objects from Halo.

        Args:
            base_url(str): This is the path of the URL, not including hostname
                or parameters.
            batch_size(int): This is the number of URLs that will be generated.
            params(dict): These are parameters that will be added to each URL.

        Returns:
            list: This returns a list of tuples, where the first item in the
                tuple is the URL path, the second is the params to be appended
                to the URL when retrieved.
        """
        url_list = []
        for page in range(1, batch_size + 1):
            params["page"] = page
            url = (path, dict(params))
            url_list.append(url)
        return url_list

    @classmethod
    def get_adjustment_factor(cls, pages, page_size, item_key):
        """Return adjustment factor, to optimize parallelization of API req.

        Args:
            pages(list): Pages from query.
            page_size(int): Number of items in a full page

        Returns:
            int: Positive or negative integer, which should be used to either
                increase or decrease the number of threads used to pull pages
                from the Halo API.
        """
        total_pages = len(pages)
        full_pages = cls.get_number_of_full_pages(pages, page_size, item_key)
        empty_pages = cls.get_number_of_empty_pages(pages, item_key)
        if empty_pages == 0:
            if total_pages == full_pages:
                adjustment_factor = 1
            else:
                adjustment_factor = 0
        elif full_pages == 0:
            adjustment_factor = -9
        else:
            adjustment_factor = -1
        return adjustment_factor

    def get_next_batch(self):
        """Gets the next batch of time-series items from the Halo API"""
        url_list = self.create_url_batch(self.start_url, self.batch_size,
                                         self.params)
        pages = self.get_pages(url_list)
        adjustment_factor = self.get_adjustment_factor(pages, self.page_size,
                                                       self.item_key)
        self.adjust_batch_size(adjustment_factor)
        items = self.sorted_items_from_pages(pages, self.item_key,
                                             self.sort_key)
        items = self.remove_duplicate_items(items, self.prior_batch_ids)
        try:
            last_item_timestamp = items[-1]['created_at']
        except IndexError:
            time.sleep(3)
            return []
        self.params["since"] = last_item_timestamp
        self.prior_batch_ids = set([x["id"] for x in items])
        return items

    @classmethod
    def get_number_of_empty_pages(cls, pages, item_key):
        """Determine number of empty pages from list of pages.

        Args:
            pages(list): List of pages as pulled from Halo API.
            item_key(str): Top-level key, below which are target items.

        Returns:
            int: Number of ampty pages from query.
        """
        empty = [page for page in pages if page[item_key] == []]
        return len(empty)

    @classmethod
    def get_number_of_full_pages(cls, pages, page_size, item_key):
        """Return the number of full pages from query.

        Args:
            pages(list): List of pages as pulled from Halo API.
            page_size(int): Expected number of items found in a full page.
            item_key(str): Top-level key, below which are target items.

        Returns:
            int: Number of full pages in query.
        """
        full = [page for page in pages if len(page[item_key]) == page_size]
        return len(full)

    def get_pages(self, url_list):
        """Map URLs to threads, return all when complete"""
        page_helper = self.get_page
        pool = ThreadPool(self.max_threads)
        results = pool.map(page_helper, url_list)
        pool.close()
        pool.join()
        return results

    def get_page(self, get_tup):
        """Gets one page's contents.

        Args:
            get_tup(tuple): First item in tuple is a string, the URL.  The
                second item is the params to be used in the query.

        Returns:
            dict: Page contents as dict
        """
        helper = HttpHelper(self.session)
        path, args = get_tup[0], get_tup[1]
        url = "{path}?{opts}".format(path=path,
                                     opts=urlencode(dict(args)))
        results = helper.get(url)
        return results

    @classmethod
    def remove_duplicate_items(cls, items_in, prior_batch_ids):
        """Return only unique itemsself.

        Args:
            items_in (list): List of dict-type items. These will be
                deduplicated by item["id"].
            prior_batch_ids (set): Set of strings, where each string is the
                id of an event which has already been yielded by __iter__().

        Returns:
            list: List of items, which is `items_in`, with duplicates removed
                and any items with item["id"] existing in `prior_batch_ids`.
        """
        items_out = []
        item_ids = set(prior_batch_ids)
        for item in items_in:
            if item["id"] not in item_ids:
                item_ids.add(item["id"])
                items_out.append(item)
            else:
                continue
        return items_out

    @classmethod
    def sorted_items_from_pages(cls, pages, item_key, sort_key):
        """Return all items, sorted by specific key.

        Args:
            pages(list): Pages from (multiple) API queries.  Raw JSON.
            item_key(str): Top-level key, below which are target items.
            sort_key(str): Key which is present in every item, by which the
                entire result will be sorted.

        Returns:
            list: List of items, extracted from pages using item_key, and
                sorted by sort_key.
        """
        items = []
        for page in pages:
            items.extend(page[item_key])
        result = sorted(items, key=operator.itemgetter(sort_key))
        return result

    @classmethod
    def verify_start_url(cls, start_url):
        """Raise CloudPassageValidation if `start_url` is invalid."""
        if start_url not in cls.allowed_urls:
            exc_msg = "This URL is unsupported for TimeSeries: %s" % start_url
            raise CloudPassageValidation(exc_msg)
        return
