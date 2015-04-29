# -*- coding: utf-8 -*-

from haystack.views import *
#from haystack.query import SearchQuerySet
from telemeta.models import *
from telemeta.forms.haystack_form import *


class HaystackSearch(FacetedSearchView):

    def __call__(self, request, type=None):
        self.type = type
        self.form_class = HaySearchForm
        return super(HaystackSearch, self).__call__(request)

    def get_query(self):
        return super(HaystackSearch, self).get_query()

    def get_results(self):
        if(self.type == 'collection'):
            return super(HaystackSearch, self).get_results().models(MediaCollection)
        else:
            return super(HaystackSearch, self).get_results().models(MediaItem)

    def extra_context(self):
        extra = super(HaystackSearch, self).extra_context()
        extra['collection_count'] = super(HaystackSearch, self).get_results().models(MediaCollection).count()
        extra['item_count'] = super(HaystackSearch, self).get_results().models(MediaItem).count()

        if extra['facets']:
            viewable_total = 0
            for viewable in extra['facets']['fields']['item_acces']:
                if viewable == 'none':
                    pass
                else:
                    viewable_total = viewable_total + viewable[1]

            extra['viewable_count'] = self.get_results().narrow('item_acces:full OR item_acces:metadata OR item_acces:mixed').count()
        if self.type == 'collection':
            extra['type'] = 'collection'
        else:
            extra['type'] = 'item'
        return extra


class HaystackAdvanceSearch(SearchView):

    def __call__(self, request, type=None):
        self.type = type
        return super(HaystackAdvanceSearch, self).__call__(request)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data

        return ''

    def get_results(self):
        if(self.type == 'collection'):
            return self.form.search().models(MediaCollection)
        else:
            return self.form.search().models(MediaItem)

    def extra_context(self):
        extra = super(HaystackAdvanceSearch, self).extra_context()
        extra['collection_count'] = self.form.search().models(MediaCollection).count()
        extra['item_count'] = self.form.search().models(MediaItem).count()
        if self.type == 'collection':
            extra['type'] = 'collection'
        else:
            extra['type'] = 'item'
        return extra
