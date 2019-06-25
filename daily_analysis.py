#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:58:19 2019

@author: maxence.faldor
"""

# topics
topics = [
 {
 'Engine': ['engine',  'fuel',  'failure',  'fire',  'aircraft',  'shut',  'etops',  'power',  'blade',  'thrust',  'bird',  'damage',  'wing',  'problem',  'boeing',  'landing',  'fan',  'oil',  'emergency',  'fail',  'twin',  'shutdown',  'turbine',  'maintenance',  'cause'],
 'Security': ['security',  'airport',  'terrorist',  'check',  'police',  'people',  'bag',  'flight',  'gun',  'weapon',  'passenger',  'staff',  'search',  'think',  'bomb',  'airside',  'uk',  'tsa',  'knife',  'threat',  'carry',  'id',  'screening'],
 'Business': ['ba',  'airline',  'company',  'year',  'cost',  'pay',  'route',  'think',  'go',  'work',  'lhr',  'business',  'time',  'staff',  'service',  'management',  'british',  'job',  'market',  'balpa',  'uk',  'easyjet'],
 'Landing': ['runway',  'landing',  'airport',  'gear',  'land',  'taxiway',  'aircraft',  'approach',  'brake',  'taxi',  'incident',  'rwy',  'wheel',  'end',  'wind',  'takeoff',  'close',  'nose',  'tower',  'damage',  'overrun',  'stop',  'tyre',  'touchdown',  'light'],
 'Plane': ['plane',  'crash',  'air',  'flight',  'report',  'passenger',  'airport',  'airline',  'airlines',  'news',  'aircraft',  'official',  'boeing',  'united',  'jet',  'aviation',  'board',  'international',  'faa',  'spokesman',  'american',  'russian',  'accident'],
 'Cabin': ['crew',  'fire',  'flight',  'cabin',  'passenger',  'door',  'emergency',  'smoke',  'pax',  'aircraft',  'evacuation',  'captain',  'seat',  'cockpit',  'slide',  'landing',  'deck',  'evacuate',  'exit',  'board',  'know',  'incident',  'open',  'land',  'problem'],
 'Company': ['ryanair',  'fr',  'fuel',  'airline',  'cost',  'mol',  'dublin',  'irish',  'aer',  'low',  'lingus',  'fare',  'pay',  'leary',  'easyjet',  'price',  'airport',  'iaa',  'company',  'ryr',  'route',  'flight',  'ireland',  'carrier']},
 {
 'Engine': ['engine',  'thrust',  'n1',  'power',  'idle',  'lever',  'epr',  'rpm',  'prop',  'start',  'turbine',  'blade',  'fan',  'failure',  'egt',  'oil',  'takeoff',  'throttle',  'fadec',  'jet',  'high',  'compressor',  'n2',  'derate',  'run'],
 'Altitude/Airspeed': ['speed',  'altitude',  'climb',  'descent',  'thrust',  'mach',  'mode',  'high',  'level',  'cruise',  'vnav',  'alt',  'ias',  'increase',  'tas',  'rate',  'wind',  'select',  'ft',  'fly',  'fmc',  'airspeed',  'max',  'change',  'low'],
 'Fuel/Tank': ['fuel',  'tank',  'pump',  'kg',  'burn',  'alternate',  'weight',  'cost',  'reserve',  'destination',  'flight',  'hour',  'cruise',  'wing',  'center',  'leak',  'flow',  'plan',  'extra',  'quantity',  'time',  'centre',  'load',  'engine',  'feed'],
 'Take-off/Landing': ['runway',  'weight',  'v1',  'takeoff',  'performance',  'distance',  'landing',  'wet',  'limit',  'obstacle',  'climb',  'gradient',  'vmcg',  'v2',  'vr',  'dry',  'stop',  'length',  'wind',  'aircraft',  'datum',  'chart',  'max',  'mutt',  'airport'],
 'Flaps': ['flap',  'slat',  'flaps',  'gear',  'speed',  'landing',  'retract',  'extend',  'vref',  'approach',  'setting',  'position',  'select',  'retraction',  'config',  'lever',  'conf',  'edge',  'configuration',  'extension',  'le',  'qrh',  'normal',  'clean',  'checklist'],
 'Brakes': ['brake',  'reverse',  'autobrake',  'landing',  'wheel',  'gear',  'braking',  'spoiler',  'reverser',  'idle',  'system',  'pressure',  'thrust',  'taxi',  'runway',  'rto',  'hydraulic',  'lever',  'pedal',  'speedbrake',  'parking',  'tyre',  'stop',  'carbon',  'nose'],
 'Equipment': ['apu',  'bleed',  'pack',  'valve',  'air',  'start',  'battery',  'switch',  'power',  'bus',  'pressure',  'system',  'pump',  'cabin',  'engine',  'ice',  'open',  'generator',  'fire',  'hydraulic',  'ac',  'supply',  'light',  'electrical',  'ground']}]

# Import
import sys
import string
import re
import datetime
from sqlalchemy import create_engine, MetaData, Table, select, update, distinct, and_
import numpy as np
import pandas as pd
import spacy

from daily_topic_classification import daily_topic_classification
from daily_organization_recognition import daily_organization_recognition
from daily_sentiment_analysis import daily_sentiment_analysis

# Usage and script arguments
if len(sys.argv) < 7:
    print('Usage: python3 pprune_daily_organization.py <dbip> <dbport> <dbusername> <dbpassword> <dbschema> <forum_id>')
    sys.exit(1)

dbip = sys.argv[1]
dbport = int(sys.argv[2])
dbusername = sys.argv[3]
dbpassword = sys.argv[4]
dbschema = sys.argv[5]
forum_id = int(sys.argv[6])

# Configure connection to database
engine = create_engine('hana+pyhdb://{}:{}@{}:{}'.format(dbusername, dbpassword, dbip, dbport))
connection = engine.connect()
metadata = MetaData(engine)

el_pprune_thread = Table('el_pprune_thread', metadata,  schema=dbschema, autoload=True)
el_pprune_post = Table('el_pprune_post', metadata,  schema=dbschema, autoload=True)

# Get out-of-date threads' thread_id
query = select([distinct(el_pprune_post.columns.thread_id)]).where(and_(el_pprune_post.columns.thread_id.in_(select([el_pprune_thread.columns.thread_id]).where(el_pprune_thread.columns.forum_id == forum_id)), el_pprune_post.columns.modified_by.is_(None)))
out_of_date_thread_id = connection.execute(query).fetchall()
out_of_date_thread_id = [r[0] for r in out_of_date_thread_id]

# Get all posts in these threads
query = select([el_pprune_post]).where(el_pprune_post.columns.thread_id.in_(out_of_date_thread_id))
post = pd.DataFrame(connection.execute(query).fetchall())
post.columns = ['post_id',
                'thread_id',
                'user',
                'date',
                'content',
                'polarity',
                'subjectivity',
                'created_by',
                'created_date',
                'modified_by',
                'modified_date']
post.dropna(subset=['content'], inplace=True)



### Clean posts' content
punctuations = string.punctuation
nlp = spacy.load('en_core_web_lg')
nlp.Defaults.stop_words |= {'like', 'maybe', 'make', 'know', 'think', 'go', 'look', 'say', 'post', 'see', 'get', 'thing'}

def clean(text, keep_url=False):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if not token.is_stop and token.text.strip() not in punctuations and token.pos_ != 'NUM':
            if token.like_url:
                if keep_url:
                    tokens.append(token.text.strip())
            else:
                tokens.append(token.lemma_.strip())
    
    return " ".join(tokens)

post['content'] = post.content.apply(lambda text: text.encode('ascii').decode('utf8'))
post['clean_content'] = post.content.apply(lambda text: re.sub(r'(\[QUOTE=.*?\]|\n|\r|\.{2,}|-{2,})', ' ', text))
post['clean_content'] = post.clean_content.apply(clean, keep_url=False)
post['clean_content'] = post.clean_content.apply(lambda text: text.encode('ascii').decode('utf8'))



now = datetime.datetime.now()
### Run daily topic classification, organization recognition and sentiment analysis
# Classify out-of-date threads into topics in EL_PPRUNE_THREAD
thread = daily_topic_classification(post, topics[forum_id])
thread = thread.where((pd.notnull(thread)), None)
for index, row in thread.iterrows():
    query = update(el_pprune_thread).values({'topic': row['topic']}).where(el_pprune_thread.columns.thread_id == row['thread_id'])
    connection.execute(query)

# Insert recognized organizations in EL_PPRUNE_ORGANIZATION
el_s_link_organization = pd.read_sql_table(table_name='el_s_link_organization', con=engine, coerce_float=False, schema=dbschema)
el_s_link_organization.dropna(subset=['link'], inplace=True)
el_s_link_organization.drop_duplicates(subset=['link'], inplace=True)
organization = daily_organization_recognition(post[post.modified_by.isna()], el_s_link_organization)
organization['created_by'] = dbusername
organization['created_date'] = now
organization.to_sql('el_pprune_organization', con=engine, if_exists='append', schema=dbschema, index=False)

# Analyse out-of-date posts sentiment (polarity and subjectivity)
post = daily_sentiment_analysis(post[post.modified_by.isna()])
for index, row in post.iterrows():
    query = update(el_pprune_post).values({'polarity': row['polarity'], 'subjectivity': row['subjectivity']}).where(el_pprune_post.columns.post_id == row['post_id'])
    connection.execute(query)



### Update MODIFIED_BY and MODIFIED_DATE columns
query = update(el_pprune_post).values({'modified_by': dbusername, 'modified_date': now}).where(el_pprune_post.columns.post_id.in_(post.post_id.to_list()))
connection.execute(query)
query = update(el_pprune_thread).values({'modified_by': dbusername, 'modified_date': now}).where(el_pprune_thread.columns.thread_id.in_(thread.thread_id.to_list()))
connection.execute(query)

