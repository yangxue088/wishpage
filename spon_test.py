# -*- coding: utf-8 -*-

no_sponsored_report = [('''holz handsäge''', '''1''', '''13'''), ('''klappsägen''', '''1''', '''12'''), ('''handsaege''', '''1''', '''7'''),
                       ('''handsäge für''', '''1''', '''8'''), ('''baum handsäge''', '''1''', '''1'''),
                       ('''klappsäge outdoor''', '''1''', '''8'''), ('''astsäge baumsäge handsäge''', '''1''', '''7'''),
                       ('''klappsäge baumsäge''', '''1''', '''3'''), ('''handsäge holz''', '''1''', '''7'''),
                       ('''japanische klappsaege''', '''1''', '''4'''), ('''baum sägen''', '''1''', '''3'''),
                       ('''japanische handsägen''', '''1''', '''3'''), ('''japanische klappsäge''', '''1''', '''4'''),
                       ('''japanische sägen''', '''1''', '''15'''), ('''klappsäge''', '''1''', '''9'''),
                       ('''klappsaege outdoor''', '''1''', '''7'''), ('''handsägen''', '''1''', '''12'''),
                       ('''hand astsäge''', '''1''', '''5'''), ('''klappsäge säge-klinge''', '''1''', '''6'''),
                       ('''camping säge''', '''2''', '''5'''), ('''handsäge fein''', '''2''', '''7'''),
                       ('''outdoor säge''', '''2''', '''4'''), ('''astsäge''', '''8''', '''14'''), ]

sponsored_report = [('''klappsäge baumsäge''', '''1''', '''3'''), ('''astsäge baumsäge handsäge''', '''1''', '''7'''),
                    ('''klappsäge outdoor''', '''1''', '''8'''), ('''holz handsäge''', '''1''', '''13'''),
                    ('''handsäge für''', '''1''', '''8'''), ('''handsaege''', '''1''', '''7'''), ('''handsäge''', '''1''', '''9'''),
                    ('''japanische handsägen''', '''1''', '''3'''), ('''klappsäge''', '''1''', '''9'''),
                    ('''handsägen''', '''1''', '''12'''), ('''handsäge holz''', '''1''', '''7'''),
                    ('''hand astsäge''', '''1''', '''5'''), ('''baum handsäge''', '''1''', '''1'''),
                    ('''japanische baumsäge''', '''1''', '''11'''), ('''baum sägen''', '''1''', '''3'''),
                    ('''klappsäge säge-klinge''', '''1''', '''6'''), ('''japanische sägen''', '''1''', '''15'''),
                    ('''klappsaege outdoor''', '''1''', '''7'''), ('''japanische klappsäge''', '''1''', '''4'''),
                    ('''japanische klappsaege''', '''1''', '''4'''), ('''klappsägen''', '''1''', '''12'''),
                    ('''handsäge fein''', '''2''', '''7'''), ('''outdoor säge''', '''2''', '''4'''),
                    ('''camping säge''', '''2''', '''5'''), ('''handsägen für holz''', '''2''', '''11'''),
                    ('''handsäge metall''', '''3''', '''2'''), ('''outdoor messer säge''', '''6''', '''2'''),
                    ('''baumsäge''', '''6''', '''7'''), ('''astsaege''', '''8''', '''3'''), ('''hand säge''', '''8''', '''2'''),
                    ('''astsäge''', '''8''', '''14'''), ('''astsägen''', '''13''', '''1'''), ('''säge''', '''16''', '''14'''), ]

search_keyword = ['''säge''', '''klappsäge outdoor''', '''handsäge fein''', '''astsägen''', '''camping säge''', '''handsäge metall''',
                  '''japanische klappsäge''', '''handsäge holz''', '''baum handsäge''', '''holz handsäge''', '''japanische handsägen''',
                  '''hand astsäge''', '''japanische sägen''', '''baum sägen''', '''kleine handsäge''', '''garten-klappsäge''',
                  '''handsäge für''', '''profi klappsäge''', '''klappsäge baumsäge''', '''astsäge baumsäge handsäge''',
                  '''japanische baumsäge''', '''klappsäge säge-klinge''', '''gartensäge''', '''outdoor messer säge''', '''hand säge''',
                  '''handsägen''', '''handsaege''', '''astsaege''', '''baumsäge''', '''outdoor säge''', '''klappsaege outdoor''',
                  '''klappsäge''', '''astsäge''', '''japanische klappsaege''', '''handsäge''', '''handsägen für holz''', '''klappsägen''', ]

sponsored_keyword = ['''outdoor messer säge''', '''hand säge''', '''handsägen''', '''handsaege''', '''astsaege''', '''baumsäge''',
                     '''outdoor säge''', '''klappsaege outdoor''', '''klappsäge''', '''astsäge''', '''japanische klappsaege''',
                     '''handsäge''', '''Klappsäge''', '''handsägen für holz''', '''klappsägen''', '''Handsägen''', '''Säge''',
                     '''klappsäge outdoor''', '''handsäge fein''', '''Astsägen''', '''camping säge''', '''handsäge metall''', '''Astsäge''',
                     '''Handsäge''', ]

same_words = [word for word in search_keyword if word in sponsored_keyword]

for word in same_words:

    print '-----------------------------------------------------------------------'
    for item in no_sponsored_report:
        if item[0] == word:
            print 'no_sponsored_report: {} {} {}'.format(item[0], item[1], item[2])
            break

    for item in sponsored_report:
        if item[0] == word:
            print 'sponsored_report: {} {} {}'.format(item[0], item[1], item[2])
            break
