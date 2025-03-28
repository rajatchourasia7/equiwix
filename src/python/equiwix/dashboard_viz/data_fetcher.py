from ..index_engine.selectors import (IndexConstituentsDateSelector,
                                      IndexLevelDateSelector)


class DataFetcher:
    def __init__(self, source):
        self.constituent_selector = IndexConstituentsDateSelector(source)
        self.level_selector = IndexLevelDateSelector(source)

    def get_index_levels(self, start_date, end_date):
        date_range = f'{start_date}:{end_date}'
        return self.level_selector.select(date=date_range)

    def get_constituents(self, start_date, end_date):
        date_range = f'{start_date}:{end_date}'
        return self.constituent_selector.select(date=date_range)
