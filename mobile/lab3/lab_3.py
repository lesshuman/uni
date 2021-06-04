#!/usr/bin/env python
# coding: utf-8

# In[24]:


from jinja2 import Environment, FileSystemLoader
import os
import pdfkit

tel = 45.43    #телефония
net = 209.82   #интернет

templates_dir = os.path.dirname('.')
env = Environment( loader = FileSystemLoader(templates_dir) )
template = env.get_template('template.html')

filename = 'schet_fin.html'
with open(filename,'w') as f:
    f.write(template.render(
    bik = '01111111',
    sch1 = '021204141241241000002',
    inn = '77731531515',
    kpp = '82947231481',
    bank = 'АО КРОНАБАНК Г. САНКТ-ПЕТЕРБУРГ',
    sch2 = '666600066666699996666',
    pol = 'ООО "000"',
    schn = '1337',
    day='14',
    month='Апреля',
    year='20',
    post = ' ООО "000", ИНН 77731531515, КПП 82947231481, 0000000 г. Санкт-Петербург ул. Аптекарская д.98 ',
    zak = 'Ӟ̵̨̫̺̪̭͕̑̎͛̀́̈́̄̒̍А̸̧̳̯̬̻̻̤̠͛̅̉̊̈К̶̨̧̟͕̫̬̜͖̳̂͋А̷̞̮̼̮̱̞̗̳̜̬̩̝̟̿͊͗́̀͠ͅЗ̸̧̧̦͓̻̞̲̼̆͐̂͆͑͐̎̍͐͆̕̚͜͝ͅЧ̷͇̮̯͂̾̌̉́͆̉̀̔͌͗̔̽͊̚И̴͈̜̐̈̓̿̓̿̀̊̔̅̌̕͝͝К̵̲͈̗͓̜͓̓̍̓̈́͂̆̍͐̌̃͘',
    osn = '№ 1249124 от 19.9.2013',
    name1 = 'Интернет',
    cost1 = net,
    name2 ='Телефония',
    cost2 = tel,
    itog = tel+net,
    itog2 = tel+net,
    n = " {}, на сумму {} руб.".format(2,tel+net),
    ruk = 'Распутин Р.Р.',
    buh = 'Распутин Р.Р'
    ))
    
pdfkit.from_file('schet_fin.html', 'out.pdf')

