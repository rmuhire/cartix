from app.model.models import *
from sqlalchemy import text
from saving_year import creation_year
from viewdata import miniQueryNgo, ngoName


class MapAnalytics:
    def __init__(self, sg, year):
        self.sg = sg
        self.year = year

    def provinceAnalytics(self):
        query = 'select count(saving_group.name)' \
                 ', sum(saving_group.member_female) '\
                 ', sum(saving_group.member_male)' \
                 ', sum(saving_group.borrowing)'\
                 ', sum(saving_group.saving)'\
                 ', province.name '\
                 'from saving_group, sector, district, province, ngo '\
                 'where sector.id = saving_group.sector_id AND ' \
                 'district.id = sector.district_id AND '\
                 'province.id = district.province_id AND '\
                 'saving_group.year = :year AND ' \
                 'saving_group.partner_id = ngo.id'

        if self.sg != ['null']:
            mini_query = miniQueryNgo(self.sg)
            query += ' AND ' + mini_query
        query += ' group by province.name order by province.name'

        sql_province = text(query)
        result = db.engine.execute(sql_province, year=self.year)
        province = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5]]
            province.append(data)

        """ bank data """
        sql_bank = text('select sum(bank.count),'
                        ' province.name from bank,'
                        ' sector,'
                        ' district,'
                        ' province'
                        ' where'
                        ' bank.sector_id = sector.id'
                        ' AND district.id = sector.district_id'
                        ' AND province.id = district.province_id'
                        ' AND bank.year=:year'
                        ' group by province.name order by province.name')
        bank = runQuery(sql_bank, self.year)

        """ mfi data """
        sql_mfi = text('select sum(mfi.count),'
                       ' province.name'
                       ' from mfi, sector, district, province'
                       ' where mfi.sector_id = sector.id'
                       ' AND district.id = sector.district_id'
                       ' AND province.id = district.province_id'
                       ' AND mfi.year = :year'
                       ' group by province.name'
                       ' order by province.name')
        mfi = runQuery(sql_mfi, self.year)

        """ umurengo sacco """

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' province.name'
                          ' from umurenge_sacco,'
                          ' sector, district, province'
                          ' where umurenge_sacco.sector_id = sector.id'
                          ' AND district.id = sector.district_id'
                          ' AND province.id = district.province_id'
                          ' AND umurenge_sacco.year=:year'
                          ' group by province.name order by province.name')

        usacco = runQuery(sql_usacco, self.year)

        """ non umurenge sacco """

        sql_nsacco = text('select sum(non_umurenge_sacco.count),'
                          ' province.name from non_umurenge_sacco,'
                          ' sector, district, province'
                          ' where non_umurenge_sacco.sector_id = sector.id AND'
                          ' district.id = sector.district_id AND'
                          ' province.id = district.province_id'
                          ' AND non_umurenge_sacco.year = :year'
                          ' group by province.name order by province.name')
        nsacco = runQuery(sql_nsacco, self.year)

        """ bank agent """
        sql_bank_agent = text('select sum(bank_agent.count),'
                              ' province.name from bank_agent, district,'
                              ' province where bank_agent.district_id = district.id'
                              ' AND province.id = district.province_id'
                              ' AND bank_agent.year =:year'
                              ' group by province.name order by province.name')
        bank_agent = runQuery(sql_bank_agent, self.year)

        """ Telco Agent """
        sql_telco_agent = text('select sum(telco_agent.count), province.name'
                               ' from telco_agent, district, province'
                               ' where telco_agent.district_id = district.id'
                               ' AND province.id = district.province_id'
                               ' AND telco_agent.year=:year'
                               ' group by province.name order by province.name')
        telco_agent = runQuery(sql_telco_agent, self.year)

        return [province, bank, mfi, usacco, nsacco, bank_agent, telco_agent]

    def districtAnalytics(self):
        query = 'select count(saving_group.name)'\
                            ', sum(saving_group.member_female) '\
                            ', sum(saving_group.member_male)'\
                            ', sum(saving_group.borrowing)'\
                            ', sum(saving_group.saving)'\
                            ', district.name '\
                            'from saving_group, sector, district, ngo '\
                            'where sector.id = saving_group.sector_id AND '\
                            'saving_group.borrowing != :x AND '\
                            'saving_group.saving != :x AND '\
                            'district.id = sector.district_id and '\
                            'saving_group.year = :year and '\
                            'saving_group.partner_id = ngo.id '

        if self.sg != ['null']:
            mini_query = miniQueryNgo(self.sg)
            query += ' AND ' + mini_query
        query += ' group by district.name order by district.name'

        sql_district = text(query)

        result = db.engine.execute(sql_district, x=-2, year=self.year)
        district = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5]]
            district.append(data)

        """ bank data """
        sql_bank = text('select sum(bank.count),'
                        ' district.name from bank,'
                        ' sector,'
                        ' district'
                        ' where'
                        ' bank.sector_id = sector.id'
                        ' AND district.id = sector.district_id'
                        ' AND bank.year=:year'
                        ' group by district.name order by district.name')
        bank = runQuery(sql_bank, self.year)

        """ mfi data """
        sql_mfi = text('select sum(mfi.count),'
                       ' district.name'
                       ' from mfi, sector, district'
                       ' where mfi.sector_id = sector.id'
                       ' AND district.id = sector.district_id'
                       ' AND mfi.year = :year'
                       ' group by district.name'
                       ' order by district.name')
        mfi = runQuery(sql_mfi, self.year)

        """ umurengo sacco """

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' district.name'
                          ' from umurenge_sacco,'
                          ' sector, district'
                          ' where umurenge_sacco.sector_id = sector.id'
                          ' AND district.id = sector.district_id'
                          ' AND umurenge_sacco.year = :year'
                          ' group by district.name order by district.name')

        usacco = runQuery(sql_usacco, self.year)

        """ non umurenge sacco """

        sql_nsacco = text('select sum(non_umurenge_sacco.count),'
                          ' district.name from non_umurenge_sacco,'
                          ' sector, district'
                          ' where non_umurenge_sacco.sector_id = sector.id AND'
                          ' district.id = sector.district_id and '
                          ' non_umurenge_sacco.year = :year'
                          ' group by district.name order by district.name')
        nsacco = runQuery(sql_nsacco, self.year)

        """ bank agent """
        sql_bank_agent = text('select sum(bank_agent.count),'
                              ' district.name from bank_agent, district'
                              ' where bank_agent.district_id = district.id'
                              ' AND bank_agent.year = :year'
                              ' group by district.name order by district.name')
        bank_agent = runQuery(sql_bank_agent, self.year)

        """ Telco Agent """
        sql_telco_agent = text('select sum(telco_agent.count), district.name'
                               ' from telco_agent, district'
                               ' where telco_agent.district_id = district.id'
                               ' AND telco_agent.year =:year'
                               ' group by district.name order by district.name')
        telco_agent = runQuery(sql_telco_agent, self.year)

        return [district, bank, mfi, usacco, nsacco, bank_agent, telco_agent]

    def sectorAnalytics(self):
        query = 'select count(saving_group.name)'\
                            ', sum(saving_group.member_female) '\
                            ', sum(saving_group.member_male)'\
                            ', sum(saving_group.borrowing)'\
                            ', sum(saving_group.saving)'\
                            ', sector.name'\
                            ', sector.district_id '\
                            'from saving_group, sector, ngo '\
                            'where sector.id = saving_group.sector_id '\
                            'AND saving_group.borrowing != :x AND '\
                            'saving_group.saving != :x and ' \
                            'saving_group.year = :year and ' \
                            'saving_group.partner_id = ngo.id '

        if self.sg != ['null']:
            mini_query = miniQueryNgo(self.sg)
            query += ' AND ' + mini_query
        query += ' group by sector.id order by sector.name'

        sql_district = text(query)

        result = db.engine.execute(sql_district, x=-2, year=self.year)
        sector = []
        for row in result:
            data = [row[0], row[1], row[2], row[3], row[4], row[5], returnDistrict(row[6])]
            sector.append(data)

        """ bank data """
        sql_bank = text('select sum(bank.count),'
                        ' sector.name from bank,'
                        ' sector'
                        ' where'
                        ' bank.sector_id = sector.id'
                        ' and bank.year = :year'
                        ' group by sector.name order by sector.name')
        bank = runQuery(sql_bank, self.year)

        """ mfi data """
        sql_mfi = text('select sum(mfi.count),'
                       ' sector.name'
                       ' from mfi, sector'
                       ' where mfi.sector_id = sector.id'
                       ' and mfi.year = :year'
                       ' group by sector.name'
                       ' order by sector.name')
        mfi = runQuery(sql_mfi, self.year)

        """ umurengo sacco """

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' sector.name'
                          ' from umurenge_sacco,'
                          ' sector'
                          ' where umurenge_sacco.sector_id = sector.id'
                          ' and umurenge_sacco.year = :year'
                          ' group by sector.name order by sector.name')

        usacco = runQuery(sql_usacco, self.year)

        """ non umurenge sacco """

        sql_nsacco = text('select sum(non_umurenge_sacco.count),'
                          ' sector.name from non_umurenge_sacco,'
                          ' sector'
                          ' where non_umurenge_sacco.sector_id = sector.id'
                          ' and non_umurenge_sacco.year = :year'
                          ' group by sector.name order by sector.name')
        nsacco = runQuery(sql_nsacco, self.year)

        return [sector, bank, mfi, usacco, nsacco]

    def json(self):

        province, bank, mfi, usacco, nsacco, bank_agent, telco_agent = MapAnalytics(self.sg, self.year).provinceAnalytics()
        district, bank_d, mfi_d, usacco_d, nsacco_d, bank_agent_d, telco_agent_d = MapAnalytics(self.sg, self.year).districtAnalytics()
        sector, bank_s, mfi_s, usacco_s, nsacco_s = MapAnalytics(self.sg, self.year).sectorAnalytics()

        # Province

        provinces = []
        for i in range(len(province)):
            data = {}
            value = province[i]
            bank_val = bank[i]
            mfi_val = mfi[i]
            usacco_val = usacco[i]
            nsacco_val = nsacco[i]
            telco_agent_val = telco_agent[i]
            bank_agent_val = bank_agent[i]
            data['Province'] = returnProvince(value[5])
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            if value[3] < 0:
                data['borrowing'] = 'N/A'
            else:
                data['borrowing'] = value[3]

            if value[4] < 0:
                data['saving'] = 'N/A'
            else:
                data['saving'] = value[4]

            data['bank'] = bank_val[0]
            data['mfi'] = mfi_val[0]
            data['usacco'] = usacco_val[0]
            data['nsacco'] = nsacco_val[0]
            data['bank_agent'] = bank_agent_val[0]
            data['telco_agent'] = telco_agent_val[0]
            provinces.append(data)

        # District

        districts = []
        for i in range(len(district)):
            data = {}
            value = district[i]
            try:
                bank_val = bank_d[i]
            except IndexError:
                bank_val = [0,0]
            try:
                mfi_val = mfi_d[i]
            except IndexError:
                mfi_val = [0,0]
            try:
                usacco_val = usacco_d[i]
            except IndexError:
                usacco_val = [0,0]
            try:
                nsacco_val = nsacco_d[i]
            except IndexError:
                nsacco_val = [0,0]

            telco_agent_val = telco_agent_d[i]
            bank_agent_val = bank_agent_d[i]
            data['District'] = value[5].title()
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            if value[3] < 0:
                data['borrowing'] = 'N/A'
            else:
                data['borrowing'] = value[3]

            if value[4] < 0:
                data['saving'] = 'N/A'
            else:
                data['saving'] = value[4]
            data['saving'] = value[4]
            data['bank'] = bank_val[0]
            data['mfi'] = mfi_val[0]
            data['usacco'] = usacco_val[0]
            data['nsacco'] = nsacco_val[0]
            data['bank_agent'] = bank_agent_val[0]
            data['telco_agent'] = telco_agent_val[0]
            districts.append(data)

        # Sector

        sectors = []
        for i in range(len(sector)):
            data = {}
            value = sector[i]
            try:
                bank_val = bank_s[i]
            except IndexError:
                bank_val = [0,0]
            try:
                mfi_val = mfi_s[i]
            except IndexError:
                mfi_val = [0,0]
            try:
                usacco_val = usacco_s[i]
            except IndexError:
                usacco_val = [0,0]

            try:
                nsacco_val = nsacco_s[i]
            except IndexError:
                nsacco_val = [0, 0]

            telco_agent_val = [0,0]
            bank_agent_val = [0,0]

            data['District'] = value[6].title()
            data['Sector'] = value[5].title()
            data['Density'] = value[0]
            data['Membership'] = value[1] + value[2]
            data['Female'] = value[1]
            data['Male'] = value[2]
            if value[3] < 0:
                data['borrowing'] = 'N/A'
            else:
                data['borrowing'] = value[3]

            if value[4] < 0:
                data['saving'] = 'N/A'
            else:
                data['saving'] = value[4]
            data['bank'] = bank_val[0]
            data['mfi'] = mfi_val[0]
            data['usacco'] = usacco_val[0]
            data['nsacco'] = nsacco_val[0]
            data['bank_agent'] = bank_agent_val[0]
            data['telco_agent'] = telco_agent_val[0]
            sectors.append(data)

        return [provinces, districts, sectors]


class ChartAnalytics:
    def __init__(self, year,ngo, province, district):
        self.year = year
        self.ngo = ngo.split(",")
        self.province = province
        self.district = district

    # Membership per gender
    def membership(self):
        query = 'select sum(member_female)'\
                ', sum(member_male) from saving_group, sector, ngo,' \
                'province, district'\
                ' where sector.id = saving_group.sector_id' \
                ' and sector.district_id = district.id' \
                ' and province.id = district.province_id'\
                ' and saving_group.year = :year'\
                ' and ngo.id = saving_group.partner_id'

        ngos = []
        if self.ngo != ['null']:
            mini_query = miniQueryNgo(self.ngo)
            query += " and " + mini_query
            for ngo in self.ngo:
                ngos.append(ngoName(ngo))

        location = ''
        if self.province != 'null':
            query += ' and province.id = :province'
            location = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

        if self.district != 'null':
            query += ' and district.id = :district'
            location = 'in {district} district' \
                       ''.format(district=get_district_name(self.district))

        title = 'Membership per Gender <br>{location}' \
                '<br><span style="font-size:10px; ' \
                'overflow: hidden;">{ngo}</span>'.format(ngo=', '.join(ngos), location=location)

        membership_sql = text(query)
        result = db.engine.execute(membership_sql, year=self.year, province=self.province, district=self.district)

        val = []
        labels = ['Female Members','Male Members']
        for row in result:
            val = [row[0], row[1]]

        data = []
        item = {}
        item['values'] = val
        item['labels'] = labels
        item['type'] = 'pie'

        data.append(item)

        return [data, title]

    # SGS_status per Intl NGOs
    def sg_status(self):

        # Supervised query
        query = 'select count(saving_group.sg_status), partner_id from saving_group,' \
                ' ngo, sector , district, province '\
                'WHERE saving_group.sg_status = :val' \
                ' AND saving_group.year=:year' \
                ' and ngo.id = saving_group.partner_id' \
                ' and saving_group.sector_id = sector.id' \
                ' and sector.district_id = district.id' \
                ' and province.id = district.province_id'

        ngos = []
        if self.ngo != ['null']:
            mini_query = miniQueryNgo(self.ngo)
            query += " and " + mini_query
            for ngo in self.ngo:
                ngos.append(ngoName(ngo))

        location = ''
        if self.province != 'null':
            query += ' and province.id = :province'
            location = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

        if self.district != 'null':
            query += ' and district.id = :district'
            location = 'in {district} district' \
                       ''.format(district=get_district_name(self.district))

        title = 'SGs Status per Intl NGOs <br>{location}' \
                '<br><span style="font-size:10px; ' \
                'overflow: hidden;">{ngo}</span>'.format(ngo=', '.join(ngos), location=location)

        query += " GROUP BY partner_id"

        supervised_sql = text(query)
        result = db.engine.execute(supervised_sql, val='Supervised', year=self.year,
                                   province=self.province, district=self.district)
        supervised = []
        i= 0
        for row in result:
            data = [row[0], getNgoName(row[1])]
            supervised.append(data)
            i = 1

        if not i:
            for ngo in self.ngo:
                supervised.append([0, getNgoName(ngo)])

        # Graduated Query
        query = 'select count(saving_group.sg_status),' \
                ' partner_id from saving_group, ngo, sector, district, province '\
                ' WHERE saving_group.sg_status = :val' \
                ' AND saving_group.year=:year' \
                ' and ngo.id = saving_group.partner_id' \
                ' and saving_group.sector_id = sector.id' \
                ' and sector.district_id = district.id' \
                ' and province.id = district.province_id'

        if self.ngo != ['null']:
            mini_query = miniQueryNgo(self.ngo)
            query += " and " + mini_query
        if self.province != 'null':
            query += ' and province.id = :province'
        if self.district != 'null':
            query += ' and district.id = :district'
        query += " GROUP BY partner_id"

        graduated_sql = text(query)
        result = db.engine.execute(graduated_sql, val='Graduated', year=self.year, province=self.province,
                                   district=self.district)
        graduated = []
        i = 0
        for row in result:
            data = [row[0], getNgoName(row[1])]
            i = 1
            graduated.append(data)

        if not i:
            for ngo in self.ngo:
                graduated.append([0, getNgoName(ngo)])

        supervised, graduated = renderStatusArray(supervised, graduated)

        # Supervised x y classification
        x = []
        y = []
        for item in supervised:
            x.append(item[1])
            y.append(item[0])

        # Json Supervised
        json_sup = {}
        json_sup['x'] = x
        json_sup['y'] = y
        json_sup['name'] = 'Supervised'
        json_sup['type'] = 'bar'

        # Graduated x y classification
        x = []
        y = []
        for item in graduated:
            x.append(item[1])
            y.append(item[0])

        json_grad = {}
        json_grad['x'] = x
        json_grad['y'] = y
        json_grad['name'] = 'Graduated'
        json_grad['type'] = 'bar'

        return [[json_sup, json_grad], title]

    # SG Savings and Loans per Intl NGOs
    def savings_loans(self):

        # Savings query
        query = 'select sum(saving_group.saving), partner_id from' \
                ' saving_group, ngo, sector, district, province '\
                'where saving_group.saving <> -1 and saving_group.year=:year ' \
                'and ngo.id = saving_group.partner_id' \
                ' and saving_group.sector_id = sector.id' \
                ' and sector.district_id = district.id' \
                ' and province.id = district.province_id'
        ngos = []
        if self.ngo != ['null']:
            mini_query = miniQueryNgo(self.ngo)
            query += " and " + mini_query
            for ngo in self.ngo:
                ngos.append(ngoName(ngo))
        location = ''
        if self.province != 'null':
            query += ' and province.id = :province'
            location = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

        if self.district != 'null':
            query += ' and district.id = :district'
            location = 'in {district} district' \
                       ''.format(district=get_district_name(self.district))

        title = 'Savings vs Loans per Intl NGOs <br>{location}' \
                '<br><span style="font-size:10px; ' \
                'overflow: hidden;">{ngo}</span>'.format(ngo=', '.join(ngos), location=location)
        query += " GROUP BY partner_id"

        saving_sql = text(query)
        result = db.engine.execute(saving_sql, year=self.year, province=self.province,
                                   district=self.district)

        saving = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            saving.append(data)

        # Loans query
        query = 'select sum(saving_group.borrowing), partner_id from saving_group,' \
                ' ngo, sector, district, province '\
                'where saving_group.borrowing <> -1 and saving_group.year=:year ' \
                'and ngo.id = saving_group.partner_id'\
                ' and saving_group.sector_id = sector.id' \
                ' and sector.district_id = district.id' \
                ' and province.id = district.province_id'

        if self.ngo != ['null']:
            mini_query = miniQueryNgo(self.ngo)
            query += " and " + mini_query
        if self.province != 'null':
            query += ' and province.id = :province'

        if self.district != 'null':
            query += ' and district.id = :district'

        query += " GROUP BY partner_id"

        loan_sql = text(query)
        result = db.engine.execute(loan_sql, year=self.year, province=self.province,
                                   district=self.district)
        loan = []
        for row in result:
            data = [row[0], getNgoName(row[1])]
            loan.append(data)

        # sort array
        saving = sortArray(saving)
        loan = sortArray(loan)

        #return [saving, loan]

        # Saving x y classification
        x = []
        y = []
        for item in saving:
            x.append(item[1])
            y.append(item[0])

        json_saving = dict()
        json_saving['x'] = x
        json_saving['y'] = y
        json_saving['name'] = 'Savings'
        json_saving['type'] = 'bar'

        # Loan x y classification
        x = []
        y = []
        for item in loan:
            x.append(item[1])
            y.append(item[0])

        json_loan = dict()
        json_loan['x'] = x
        json_loan['y'] = y
        json_loan['name'] = 'Loans'
        json_loan['type'] = 'bar'

        return [[json_saving, json_loan], title]

    # Saving Group creation year
    def creation(self):
        years = creation_year()
        data = []
        for year in years:
            yearlist = list()

            query = 'select count(saving_group.id), saving_group.partner_id from saving_group, ngo '\
                    'where saving_group.year_of_creation = :year and saving_group.year=:year_s ' \
                    'and ngo.id = saving_group.partner_id'
            location = ''
            if self.province != 'null':
                query = 'select count(saving_group.id), saving_group.partner_id from saving_group, ngo,' \
                        'sector, district, province ' \
                        'where saving_group.year_of_creation = :year' \
                        ' and saving_group.year=:year_s' \
                        ' and ngo.id = saving_group.partner_id' \
                        ' and saving_group.sector_id = sector.id' \
                        ' and sector.district_id = district.id' \
                        ' and province.id = district.province_id' \
                        ' and province.id = :province'

                location = 'in {province} province' \
                           ''.format(province=get_province_name(self.province))

            if self.district != 'null':
                query = 'select count(saving_group.id), saving_group.partner_id from saving_group, ngo,' \
                        'sector, district, province ' \
                        'where saving_group.year_of_creation = :year' \
                        ' and saving_group.year=:year_s' \
                        ' and ngo.id = saving_group.partner_id' \
                        ' and saving_group.sector_id = sector.id' \
                        ' and sector.district_id = district.id' \
                        ' and province.id = district.province_id' \
                        ' and province.id = :province' \
                        ' and district.id = :district'

                location = 'in {district} district' \
                           ''.format(district=get_district_name(self.district))

            if self.ngo != ['null']:
                mini_query = miniQueryNgo(self.ngo)
                query += " and " + mini_query
            query += " GROUP BY partner_id"
            year_sql = text(query)
            result = db.engine.execute(year_sql, year=year, year_s=self.year,
                                       province=self.province,
                                       district=self.district)
            for row in result:
                val = [row[0], getNgoName(row[1])]
                yearlist.append(val)

            data.append(sortArray(yearlist))

        trace = []
        for i in range(len(data)):
            x = []
            y = []
            json = dict()
            for item in data[i]:
                x.append(item[1])
                y.append(item[0])
            json['x'] = x
            json['y'] = y
            json['name'] = years[i]
            json['type'] = 'bar'
            trace.append(json)
        title = 'SGs Creation year/Internatonal NGOs <br>{location}' \
                ''.format(location=location)

        return [trace, title]

    def savingPerIntNgo(self):
        query = 'select count(saving_group.id),'\
                ' ngo.id,'\
                ' ngo.name'\
                ' from saving_group,'\
                ' ngo, sector, district, province' \
                ' where saving_group.partner_id = ngo.id'\
                ' AND saving_group.year = :year' \
                ' and sector.id = saving_group.sector_id' \
                ' and sector.district_id = district.id' \
                ' and province.id = district.province_id'

        if self.ngo != ['null']:
            mini_query = miniQueryNgo(self.ngo)
            query += " and " + mini_query

        location = ''
        if self.province != 'null':
            query += ' and province.id = :province'
            location = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

        if self.district != 'null':
            query += ' and district.id = :district'
            location = 'in {district} district' \
                       ''.format(district=get_district_name(self.district))

        query += " group by ngo.id"
        sql = text(query)

        title = 'SGs per International NGOs <br>{location}' \
                '<br>'.format(location=location)

        result = db.engine.execute(sql, year=self.year, province=self.province,
                                   district=self.district)
        values = list()
        labels = list()
        for row in result:
            values.append(row[0])
            labels.append(row[2])

        json = dict()
        json['values'] = values
        json['labels'] = labels
        json['type'] = 'pie'

        return [[json], title]

    def localPerIntNgo(self):
        sql = text('select distinct(funding_id)'
                   ' from saving_group'
                   ' where year = :year')
        result = db.engine.execute(sql, year=self.year)
        data = list()
        for row in result:
            funding_id = row[0]
            x = list()
            y = list()

            query = 'select distinct(saving_group.partner_id),'\
                    ' count(saving_group.id)'\
                    ' from saving_group, ngo, sector, district, province'\
                    ' where saving_group.funding_id = :funding_id' \
                    ' and saving_group.year=:year' \
                    ' AND saving_group.partner_id = ngo.id' \
                    ' and sector.id = saving_group.sector_id' \
                    ' and sector.district_id = district.id' \
                    ' and province.id = district.province_id'

            if self.ngo != ['null']:
                mini_query = miniQueryNgo(self.ngo)
                query += " and " + mini_query

            location = ''
            if self.province != 'null':
                query += ' and province.id = :province'
                location = 'in {province} province' \
                           ''.format(province=get_province_name(self.province))

            if self.district != 'null':
                query += ' and district.id = :district'
                location = 'in {district} district' \
                           ''.format(district=get_district_name(self.district))

            query += " group by partner_id"



            sql = text(query)
            re = db.engine.execute(sql, funding_id=funding_id, year=self.year, province=self.province,
                                   district=self.district)
            for item in re:
                x.append(getNgoName(item[0]))
                y.append(item[1])
            json = dict()
            json['x'] = x
            json['y'] = y
            json['name'] = getNgoName(funding_id)
            json['type'] = 'bar'
            data.append(json)

        title = 'Local NGOs SGs count per Intl NGOs <br>{location}'.format(location=location)
        return [data, title]

    def sgFinancialInstitution(self):
        sql_sg = text('select count(saving_group.id),'
                      ' province.name'
                      ' from saving_group,'
                      ' sector, district,'
                      ' province where sector.id = saving_group.sector_id'
                      ' AND district.id = sector.district_id'
                      ' AND province.id = district.province_id'
                      ' AND saving_group.year=:year'
                      ' group by province.name'
                      ' order by province.name')

        if self.province != 'null':
            sql_sg = text('select count(saving_group.id),'
                          ' district.name'
                          ' from saving_group,'
                          ' sector, district,'
                          ' province where sector.id = saving_group.sector_id'
                          ' AND district.id = sector.district_id'
                          ' AND province.id = district.province_id'
                          ' AND province.id = :province'
                          ' AND saving_group.year=:year'
                          ' group by district.name'
                          ' order by district.name')

        if self.district != 'null':
            sql_sg = text('select count(saving_group.id),'
                          ' sector.name'
                          ' from saving_group,'
                          ' sector, district,'
                          ' province where sector.id = saving_group.sector_id'
                          ' AND district.id = sector.district_id'
                          ' AND province.id = district.province_id'
                          ' AND province.id = :province'
                          ' AND district.id = :district'
                          ' AND saving_group.year=:year'
                          ' group by sector.name'
                          ' order by sector.name')

        result = db.engine.execute(sql_sg, year=self.year, province=self.province,
                                   district=self.district)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        # Bank Data
        sql_banks = text('select sum(bank.count),'
                         ' province.name'
                         ' from bank,'
                         ' sector,'
                         ' district,'
                         ' province'
                         ' where sector.id = bank.sector_id'
                         ' AND district.id = sector.district_id'
                         ' AND province.id = district.province_id'
                         ' AND bank.year=:year'
                         ' group by province.name order'
                         ' by province.name')

        if self.province != 'null':
            sql_banks = text('select sum(bank.count),'
                             ' district.name'
                             ' from bank,'
                             ' sector,'
                             ' district,'
                             ' province'
                             ' where sector.id = bank.sector_id'
                             ' AND district.id = sector.district_id'
                             ' AND province.id = district.province_id'
                             ' AND province.id = :province'
                             ' AND bank.year=:year'
                             ' group by district.name order'
                             ' by district.name')

        if self.district != 'null':
            sql_banks = text('select sum(bank.count),'
                             ' sector.name'
                             ' from bank,'
                             ' sector,'
                             ' district,'
                             ' province'
                             ' where sector.id = bank.sector_id'
                             ' AND district.id = sector.district_id'
                             ' AND province.id = district.province_id'
                             ' AND province.id = :province'
                             ' AND district.id = :district'
                             ' AND bank.year=:year'
                             ' group by sector.name order'
                             ' by sector.name')

        result = db.engine.execute(sql_banks, year=self.year, province=self.province,
                                   district=self.district)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_bank = dict()
        json_bank['x'] = x
        json_bank['y'] = y
        json_bank['name'] = 'Banks'
        json_bank['type'] = 'bar'


        # mfi
        sql_mfi = text('select sum(mfi.count),'
                       ' province.name'
                       ' from mfi, sector, district, province '
                       'where sector.id = mfi.sector_id AND'
                       ' district.id = sector.district_id AND'
                       ' province.id = district.province_id and mfi.year=:year group by'
                       ' province.name order by province.name')

        if self.province != 'null':
            sql_mfi = text('select sum(mfi.count),'
                           ' district.name'
                           ' from mfi, sector, district, province '
                           'where sector.id = mfi.sector_id AND'
                           ' district.id = sector.district_id AND'
                           ' province.id = district.province_id'
                           ' AND province.id = :province'
                           ' and mfi.year=:year group by'
                           ' district.name order by district.name')

        if self.district != 'null':
            sql_mfi = text('select sum(mfi.count),'
                           ' sector.name'
                           ' from mfi, sector, district, province '
                           'where sector.id = mfi.sector_id AND'
                           ' district.id = sector.district_id AND'
                           ' province.id = district.province_id'
                           ' AND province.id = :province'
                           ' AND district.id = :district'
                           ' and mfi.year=:year group by'
                           ' sector.name order by sector.name')

        result = db.engine.execute(sql_mfi, year=self.year, province=self.province,
                                   district=self.district)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_mfi = dict()
        json_mfi['x'] = x
        json_mfi['y'] = y
        json_mfi['name'] = 'MFIs'
        json_mfi['type'] = 'bar'

        # umurenge sacco

        sql_usacco = text('select sum(umurenge_sacco.count),'
                          ' province.name'
                          ' from umurenge_sacco, sector, district, province'
                          ' where sector.id = umurenge_sacco.sector_id AND'
                          ' district.id = sector.district_id AND'
                          ' province.id = district.province_id and umurenge_sacco.year=:year'
                          ' group by province.name'
                          ' order by province.name')

        if self.province != 'null':
            sql_usacco = text('select sum(umurenge_sacco.count),'
                              ' district.name'
                              ' from umurenge_sacco, sector, district, province'
                              ' where sector.id = umurenge_sacco.sector_id AND'
                              ' district.id = sector.district_id AND'
                              ' province.id = district.province_id'
                              ' AND province.id = :province'
                              ' and umurenge_sacco.year=:year'
                              ' group by district.name'
                              ' order by district.name')

        if self.district != 'null':
            sql_usacco = text('select sum(umurenge_sacco.count),'
                              ' sector.name'
                              ' from umurenge_sacco, sector, district, province'
                              ' where sector.id = umurenge_sacco.sector_id AND'
                              ' district.id = sector.district_id AND'
                              ' province.id = district.province_id'
                              ' AND province.id = :province'
                              ' AND district.id = :district'
                              ' and umurenge_sacco.year=:year'
                              ' group by sector.name'
                              ' order by sector.name')

        result = db.engine.execute(sql_usacco, year=self.year,
                                   province=self.province,
                                   district=self.district)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_usacco = dict()
        json_usacco['x'] = x
        json_usacco['y'] = y
        json_usacco['name'] = 'Umurenge Sacco'
        json_usacco['type'] = 'bar'

        # Non - Umurenge Sacco

        sql_nusacco = text('select sum(non_umurenge_sacco.count),'
                           ' province.name'
                           ' from non_umurenge_sacco, sector, district, province'
                           ' where sector.id = non_umurenge_sacco.sector_id'
                           ' AND district.id = sector.district_id '
                           'AND province.id = district.province_id '
                           'and non_umurenge_sacco.year=:year '
                           'group by province.name '
                           'order by province.name')

        location = ''
        if self.province != 'null':
            location = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

            sql_nusacco = text('select sum(non_umurenge_sacco.count),'
                               ' district.name'
                               ' from non_umurenge_sacco, sector, district, province'
                               ' where sector.id = non_umurenge_sacco.sector_id'
                               ' AND district.id = sector.district_id '
                               'AND province.id = district.province_id '
                               ' AND province.id = :province '
                               'and non_umurenge_sacco.year=:year '
                               'group by district.name '
                               'order by district.name')

        if self.district != 'null':
            sql_nusacco = text('select sum(non_umurenge_sacco.count),'
                               ' sector.name'
                               ' from non_umurenge_sacco, sector, district, province'
                               ' where sector.id = non_umurenge_sacco.sector_id'
                               ' AND district.id = sector.district_id '
                               'AND province.id = district.province_id '
                               ' AND province.id = :province'
                               ' AND district.id = :district '
                               ' and non_umurenge_sacco.year=:year '
                               'group by sector.name '
                               'order by sector.name')

            location = 'in {district} district' \
                       ''.format(district=get_district_name(self.district))

        result = db.engine.execute(sql_nusacco, year=self.year,
                                   province=self.province,
                                   district=self.district)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_nusacco = dict()
        json_nusacco['x'] = x
        json_nusacco['y'] = y
        json_nusacco['name'] = 'Non-Umurenge Sacco'
        json_nusacco['type'] = 'bar'

        title = 'SGs and Financial Institution <br>{location}' \
                '<br>'.format(location=location)

        return [[json_sg, json_bank, json_mfi, json_usacco, json_nusacco], title]

    def sgTelcoAgent(self):
        # telco agent
        sql_telco = text('select sum(telco_agent.count),'
                         ' province.name'
                         ' from telco_agent, province, district'
                         ' where telco_agent.district_id = district.id '
                         'and district.province_id = province.id '
                         'and telco_agent.year=:year '
                         'group by province.name '
                         'order by province.name')

        if self.province != 'null':
            sql_telco = text('select sum(telco_agent.count),'
                             ' district.name'
                             ' from telco_agent, province, district'
                             ' where telco_agent.district_id = district.id '
                             'and district.province_id = province.id '
                             'and province.id = :province '
                             'and telco_agent.year=:year '
                             'group by district.name '
                             'order by district.name')

        result = db.engine.execute(sql_telco, year=self.year, province=self.province)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_telco = dict()
        json_telco['x'] = x
        json_telco['y'] = y
        json_telco['name'] = 'Telco Agents'
        json_telco['type'] = 'bar'

        # bank agent
        sql_bank = text('select sum(bank_agent.count),'
                         ' province.name'
                         ' from bank_agent, province, district'
                         ' where bank_agent.district_id = district.id '
                         'and district.province_id = province.id '
                         'and bank_agent.year=:year '
                         'group by province.name '
                         'order by province.name')

        if self.province != 'null':
            sql_bank = text('select sum(bank_agent.count),'
                            ' district.name'
                            ' from bank_agent, province, district'
                            ' where bank_agent.district_id = district.id '
                            'and district.province_id = province.id '
                            'and province.id = :province '
                            'and bank_agent.year=:year '
                            'group by district.name '
                            'order by district.name')

        result = db.engine.execute(sql_bank, year=self.year, province=self.province)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_bank = dict()
        json_bank['x'] = x
        json_bank['y'] = y
        json_bank['name'] = 'Bank Agents'
        json_bank['type'] = 'bar'

        # sg

        sql_sg = text('select count(saving_group.id),'
                      ' province.name'
                      ' from saving_group,'
                      ' sector, district,'
                      ' province where sector.id = saving_group.sector_id'
                      ' AND district.id = sector.district_id'
                      ' AND province.id = district.province_id'
                      ' AND saving_group.year = :year'
                      ' group by province.name'
                      ' order by province.name')
        province = ''
        if self.province != 'null':
            province = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

            sql_sg = text('select count(saving_group.id),'
                          ' district.name'
                          ' from saving_group,'
                          ' sector, district,'
                          ' province where sector.id = saving_group.sector_id'
                          ' AND district.id = sector.district_id'
                          ' AND province.id = district.province_id'
                          ' AND province.id = :province'
                          ' AND saving_group.year = :year'
                          ' group by district.name'
                          ' order by district.name')

        result = db.engine.execute(sql_sg, year=self.year, province=self.province)
        x = list()
        y = list()
        for row in result:
            y.append(row[0])
            x.append(row[1])
        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        title = 'SGs, Banks and Telco Agents <br>{province}' \
                '<br>'.format(province=province)

        return [[json_sg, json_telco, json_bank], title]

    def finscope(self):
        sg_2012 = text('select sum(member_female), sum(member_male) '
                  'from saving_group'
                  ' where year_of_creation = 2012')
        if self.province != 'null':
            sg_2012 = text('select sum(saving_group.member_female), sum(saving_group.member_male) '
                           'from saving_group, sector, district, province'
                           ' where saving_group.year_of_creation = 2012'
                           ' and saving_group.sector_id = sector.id'
                           ' and district.id = sector.district_id'
                           ' and province.id = district.province_id'
                           ' and province.id = :province')

        result = db.engine.execute(sg_2012, province=self.province)
        x = list()
        y = list()
        for row in result:
            sum_sg_2012 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs vs Finscope 2012')
            y.append(sum_sg_2012)

        sg_2015 = text('select sum(member_female),'
                       ' sum(member_male)'
                  ' from saving_group'
                  ' where year_of_creation = 2015')

        if self.province != 'null':
            sg_2015 = text('select sum(saving_group.member_female), sum(saving_group.member_male) '
                           'from saving_group, sector, district, province'
                           ' where saving_group.year_of_creation = 2015'
                           ' and saving_group.sector_id = sector.id'
                           ' and district.id = sector.district_id'
                           ' and province.id = district.province_id'
                           ' and province.id = :province')

        result = db.engine.execute(sg_2015, province=self.province)
        for row in result:
            sum_sg_2015 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs vs Finscope 2015')
            y.append(sum_sg_2015)

        json_sg = dict()
        json_sg['x'] = x
        json_sg['y'] = y
        json_sg['name'] = 'SGs'
        json_sg['type'] = 'bar'

        o_informal_2012 = text('select sum(other_informal)'
                               ' from finscope where year = 2012')
        if self.province != 'null':
            o_informal_2012 = text('select sum(finscope.other_informal)'
                                   ' from finscope, district, province where'
                                   ' finscope.year = 2012'
                                   ' and finscope.district_id = district.id'
                                   ' and province.id = district.province_id'
                                   ' and province.id = :province')
        result = db.engine.execute(o_informal_2012, province=self.province)
        x = list()
        y = list()
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2012
            x.append('SGs vs Finscope 2012')
            y.append(remain)

        o_informal_2015 = text('select sum(other_informal)'
                               ' from finscope where year = 2012')

        if self.province != 'null':
            o_informal_2015 = text('select sum(finscope.other_informal)'
                                   ' from finscope, district, province where'
                                   ' finscope.year = 2015'
                                   ' and finscope.district_id = district.id'
                                   ' and province.id = district.province_id'
                                   ' and province.id = :province')

        result = db.engine.execute(o_informal_2015, province=self.province)
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2015
            x.append('SGs vs Finscope 2015')
            y.append(remain)

        json_other = dict()
        json_other['x'] = x
        json_other['y'] = y
        json_other['name'] = 'Other Informal'
        json_other['type'] = 'bar'

        # Excluded data
        exluded_2012 = text('select sum(excluded) from finscope where year = 2012')
        if self.province != 'null':
            exluded_2012 = text('select sum(finscope.excluded) from finscope, district,'
                                ' province'
                                ' where finscope.year = 2012'
                                ' and finscope.district_id = district.id'
                                ' and province.id = district.province_id'
                                ' and province.id = :province')
        result = db.engine.execute(exluded_2012, province=self.province)
        x = list()
        y = list()
        for row in result:
            x.append('SGs vs Finscope 2012')
            y.append(row[0])

        exluded_2015 = text('select sum(excluded) from finscope where year = 2015')
        province = ''
        if self.province != 'null':
            province = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))
            exluded_2015 = text('select sum(finscope.excluded) from finscope, district,'
                                ' province'
                                ' where finscope.year = 2015'
                                ' and finscope.district_id = district.id'
                                ' and province.id = district.province_id'
                                ' and province.id = :province')
        result = db.engine.execute(exluded_2015, province=self.province)
        for row in result:
            x.append('SGs vs Finscope 2015')
            y.append(row[0])

        json_excluded = dict()
        json_excluded['x'] = x
        json_excluded['y'] = y
        json_excluded['name'] = 'Excluded'
        json_excluded['type'] = 'bar'

        title = 'SGs members vs Finscope <br>{province}' \
                '<br>'.format(province=province)

        return [[json_sg, json_other, json_excluded], title]

    def finscope_sg(self):
        sg_2012 = text('select sum(member_female), sum(member_male) '
                       'from saving_group'
                       ' where year_of_creation = 2012')

        if self.province != 'null':
            sg_2012 = text('select sum(saving_group.member_female), sum(saving_group.member_male) '
                           'from saving_group, sector, district, province'
                           ' where saving_group.year_of_creation = 2012'
                           ' and saving_group.sector_id = sector.id'
                           ' and district.id = sector.district_id'
                           ' and province.id = district.province_id'
                           ' and province.id = :province')

        result = db.engine.execute(sg_2012, province=self.province)
        x = list()
        y = list()
        for row in result:
            sum_sg_2012 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs 2012')
            y.append(sum_sg_2012)

        o_informal_2012 = text('select sum(other_informal)'
                               ' from finscope where year = 2012')
        if self.province != 'null':
            o_informal_2012 = text('select sum(finscope.other_informal)'
                                   ' from finscope, district, province where finscope.year = 2012'
                                   ' and finscope.district_id = district.id'
                                   ' and province.id = district.province_id'
                                   ' and province.id = :province')
        result = db.engine.execute(o_informal_2012, province=self.province)
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2012
            x.append('Other Informal 2012')
            y.append(remain)

        json_2012 = dict()
        json_2012['values'] = y
        json_2012['labels'] = x
        json_2012['type'] = 'pie'

        """ 2015  """
        sg_2015 = text('select sum(member_female), sum(member_male) '
                       'from saving_group'
                       ' where year_of_creation = 2015')
        if self.province != 'null':
            sg_2015 = text('select sum(saving_group.member_female), sum(saving_group.member_male) '
                           'from saving_group, sector, district, province'
                           ' where saving_group.year_of_creation = 2015'
                           ' and saving_group.sector_id = sector.id'
                           ' and district.id = sector.district_id'
                           ' and province.id = district.province_id'
                           ' and province.id = :province')
        result = db.engine.execute(sg_2015, province=self.province)
        x = list()
        y = list()
        for row in result:
            sum_sg_2015 = convertNonType(row[0]) + convertNonType(row[1])
            x.append('SGs 2015')
            y.append(sum_sg_2015)

        o_informal_2015 = text('select sum(other_informal)'
                               ' from finscope where year = 2015')
        province = ''
        if self.province != 'null':
            o_informal_2015 = text('select sum(finscope.other_informal)'
                                   ' from finscope, district, province where finscope.year = 2015'
                                   ' and finscope.district_id = district.id'
                                   ' and province.id = district.province_id'
                                   ' and province.id = :province')
            province = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))
        result = db.engine.execute(o_informal_2015, province=self.province)
        for row in result:
            remain = convertNonType(row[0]) - sum_sg_2015
            x.append('Other Informal 2015')
            y.append(remain)

        json_2015 = dict()
        json_2015['values'] = y
        json_2015['labels'] = x
        json_2015['type'] = 'pie'

        title_2012 = 'Finscope: Other Informal Vs SGs member 2012 <br>{province}' \
                '<br>'.format(province=province)

        title_2015 = 'Finscope: Other Informal Vs SGs member 2015 <br>{province}' \
                '<br>'.format(province=province)

        return [[json_2012, title_2012], [json_2015, title_2015]]

    def finscope_all(self, year):
        finscope = text('select sum(finscope.banked), sum(finscope.other_formal),'
                        ' sum(finscope.other_informal), sum(finscope.excluded),'
                        ' province.name from finscope, province,'
                        ' district where finscope.district_id = district.id'
                        ' and province.id = district.province_id'
                        ' and finscope.year = :year'
                        ' group by province.name order by province.name')

        if self.province != 'null':
            finscope = text('select sum(finscope.banked), sum(finscope.other_formal),'
                            ' sum(finscope.other_informal), sum(finscope.excluded),'
                            ' district.name from finscope, province,'
                            ' district where finscope.district_id = district.id'
                            ' and province.id = district.province_id'
                            ' and province.id = :province'
                            ' and finscope.year = :year'
                            ' group by district.name order by district.name')

        result = db.engine.execute(finscope, year=year, province=self.province)
        x = list()
        banked = list()
        other_formal = list()
        other_informal = list()
        excluded = list()
        for row in result:
            x.append(row[4])
            banked.append(row[0])
            other_formal.append(row[1])
            other_informal.append(row[2])
            excluded.append(row[3])

        sgs = text('select sum(saving_group.member_female),'
                   ' sum(saving_group.member_male), province.name'
                   ' from saving_group, province, district, sector'
                   ' where saving_group.sector_id = sector.id'
                   ' and sector.district_id = district.id'
                   ' and district.province_id = province.id'
                   ' and saving_group.year_of_creation = :year'
                   ' group by province.name order by province.name')

        province = ''
        if self.province != 'null':
            sgs = text('select sum(saving_group.member_female),'
                       ' sum(saving_group.member_male), district.name'
                       ' from saving_group, province, district, sector'
                       ' where saving_group.sector_id = sector.id'
                       ' and sector.district_id = district.id'
                       ' and district.province_id = province.id'
                       ' and province.id = :province'
                       ' and saving_group.year_of_creation = :year'
                       ' group by district.name order by district.name')

            province = 'in {province} province' \
                       ''.format(province=get_province_name(self.province))

        result = db.engine.execute(sgs, year=year, province=self.province)
        sg = list()
        for row in result:
            sg.append(convertNonType(row[0]) + convertNonType(row[1]))


        """ JSon Banked """
        json_banked = dict()
        json_banked['x'] = x
        json_banked['y'] = banked
        json_banked['name'] = 'Banked'
        json_banked['type'] = 'bar'

        """ Json Other Formal """
        json_other_formal = dict()
        json_other_formal['x'] = x
        json_other_formal['y'] = other_formal
        json_other_formal['name'] = 'Other Formal'
        json_other_formal['type'] = 'bar'

        """ Json Other informal """
        json_other_informal = dict()
        json_other_informal['x'] = x
        json_other_informal['y'] = other_informal
        json_other_informal['name'] = 'Other Infomal'
        json_other_informal['type'] = 'bar'

        """ Json Excluded """
        json_excluded = dict()
        json_excluded['x'] = x
        json_excluded['y'] = excluded
        json_excluded['name'] = 'Excluded'
        json_excluded['type'] = 'bar'

        """ Json SGs """
        json_sgs = dict()
        json_sgs['x'] = x
        json_sgs['y'] = sg
        json_sgs['name'] = 'SGs'
        json_sgs['type'] = 'bar'

        """ Calculate other informal """
        val = list()
        for i in range(len(sg)):
            val.append(convertNonType(other_informal[i]) - convertNonType(sg[i]))

        json_other_informal['y'] = val

        title = 'Finscope {year} <br>{province}' \
                     '<br>'.format(province=province, year=year)

        return [[json_banked, json_other_formal, json_other_informal, json_excluded, json_sgs], title]


class NumberAnalytics:
    def __init__(self, year):
        self.year = year

    def numbers(self):
        sql_number =  text('select count(id),'
                           ' sum(member_female),'
                           ' sum(member_male),'
                           ' sum(saving),'
                           ' sum(borrowing)'
                           ' from saving_group'
                           ' where year = :year')
        result = db.engine.execute(sql_number, year = self.year)
        if result:
            for row in result:
                if row[1] is None:
                    return [0,0,0,0]
                data = [row[0],row[1] + row[2], row[3], row[4]]
            return data


def convertNonType(val):
    try:
        val = int(val)
    except TypeError:
        val = 0
        return val
    return val


def returnProvince(name):
    val = ['kigali', 'north', 'south', 'west', 'east']
    data = ['Kigali City', 'Northern', 'Southern', 'Western', 'Eastern']

    for i in range(len(val)):
        if name == val[i]:
            return data[i]


def returnDistrict(id):
    district = text('select name from district where id = :id')
    result = db.engine.execute(district, id=id)

    for row in result:
        return row[0]


def renderStatusArray(supervised, graduated):
    i = 0
    for x in graduated:
        for y in supervised:
            if x[1] == y[1]:
                i = 1
            val = x[1]
        if i == 0:
            supervised.append([0, val])
        i = 0

    i = 0
    for x in supervised:
        for y in graduated:
            if x[1] == y[1]:
                i = 1
            val = x[1]
        if i == 0:
            graduated.append([0, val])
        i = 0

    return [sortArray(supervised),sortArray(graduated)]


def sortArray(list):
    sorted_array =  sorted(list, key=lambda x: x[1])
    return sorted_array


def getNgoName(id):
    ngo = text('select name from ngo where id = :id')
    result = db.engine.execute(ngo, id=id)
    for row in result:
        return row[0]


def get_province_name(id):
    province = text('select name from province where id = :id')
    result = db.engine.execute(province, id=id)
    for row in result:
        return row[0]


def get_district_name(id):
    district = text('select name from district where id = :id')
    result = db.engine.execute(district, id=id)
    for row in result:
        return row[0]


def listNgo():
    ngo = text('select distinct(saving_group.partner_id),'
               ' ngo.name from saving_group,'
               ' ngo where saving_group.partner_id = ngo.id')
    result = db.engine.execute(ngo, id=id)
    data = list()
    for row in result:
        json = dict()
        json['id'] = row[0]
        json['name'] = row[1]
        data.append(json)
    return data


def runQuery(query, year):
    result = db.engine.execute(query, year=year)
    data = list()
    for row in result:
        data.append([row[0], row[1]])

    return data


