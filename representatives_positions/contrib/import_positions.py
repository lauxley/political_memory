# coding: utf-8

import csv
import django
from django.apps import apps
from django.db import transaction
import logging
import sys
import re

from representatives_positions.models import Position
from representatives.models import Representative

logger = logging.getLogger(__name__)


class PositionImporter:
    def __init__(self):
        self.rep_cache = {}

    def get_rep(self, first_name, last_name):
        key = '%s %s' % (first_name, last_name)
        rep = self.rep_cache.get(key, None)

        if rep is None:
            try:
                rep = Representative.objects.get(first_name=first_name,
                    last_name=last_name)
                self.rep_cache[key] = rep
            except Representative.DoesNotExist:
                rep = None

        return rep

    def import_row(self, row):
        if len(row['date']) == 0:
            logger.warn('Cannot import dateless position for %s %s on URL %s' %
                (row['first_name'], row['last_name'], row['url']))
            return False

        rep = self.get_rep(row['first_name'], row['last_name'])
        if rep is None:
            logger.warn('Could not find rep %s %s' % (row['first_name'],
                row['last_name']))
            return False

        text = re.sub('(^<p>|</p>$)', '', row['content'])
        if row['title'] is not None and len(row['title']) > 0:
            text = '%s\n%s' % (row['title'], text)

        try:
            position = Position.objects.get(representative=rep,
                link=row['url'])
        except Position.DoesNotExist:
            position = Position(
                representative=rep,
                link=row['url'],
                datetime=row['date'],
                text=text,
                published=True
            )
            position.save()
            logger.info('Created position for %s %s on URL %s' % (
                row['first_name'], row['last_name'], row['url']))

        return True


def main(stream=None):
    """
    Imports positions from an old memopol instance.

    Usage:
        cat positions.csv | memopol_import_positions

    The input CSV file should be generated by the following query:
        SELECT CONCAT(o.content, '|', o.url, '|', o.title, '|', ro.date, '|',
            r.first_name, '|', r.last_name)
        FROM reps_opinion o
        INNER JOIN reps_opinionrep ro ON ro.opinion_id = o.id
        INNER JOIN reps_representative r ON r.id = ro.representative_id
        WHERE o.institution='EU'

    """

    if not apps.ready:
        django.setup()

    importer = PositionImporter()
    rejected = []
    imported = 0

    reader = csv.DictReader(stream or sys.stdin, delimiter='|', fieldnames=[
        'content',
        'url',
        'title',
        'date',
        'first_name',
        'last_name'
    ], quoting=csv.QUOTE_NONE)

    for row in reader:
        if not importer.import_row(row):
            rejected.append(row)
        else:
            imported = imported + 1

    logger.info('%d rows imported, %d rows rejected', imported, len(rejected))

