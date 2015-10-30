# coding: utf-8

# This file is part of memopol.
#
# memopol is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# memopol is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

from django.conf.urls import url

from . import views

urlpatterns = [
    # Dossier detail by dossier pk
    url(
        r'^(?P<pk>\d+)$',
        views.dossier_detail,
        name='dossier-detail'
    ),
    # List all dossiers by default
    url(
        r'',
        views.dossier_index,
        name='dossier-index'
    ),
]