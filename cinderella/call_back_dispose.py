import sql
import time
from push_client import PushClient

class Dispose:
    def __init__(self, config):
        self._sql = sql.Sql(config['host'], config['port'], config['user'], config['pwd'], config['db'])
        self._sql.connect_sql()
        self._client = PushClient(config['clinet_ip'], config['push_port'], config['req_port'])
        self._last_voucher_no = 0

    def _get_agent_id(self, promo_code):
        sql_str = "SELECT account_id "\
                  "FROM accounts "\
                  "WHERE promo_code = '{}'".format(promo_code)
        rowcount, results = self._sql.query_sql(sql_str)
        return results[0][0] if rowcount else ' '

    def _get_agent_info(self, account_id):
        sql_str = "SELECT account_id, agent_id, create_datetime, status "\
                  "FROM accounts "\
                  "WHERE agent_id = '{}'".format(account_id)
        return self._sql.query_sql(sql_str)

    def _query_accounts(self, account_id):
        sql_str = "SELECT full_name, birthday, country, province, city, phone, type, promo_code "\
                  "FROM accounts "\
                  "WHERE account_id = '{}'".format(account_id)
        return self._sql.query_sql(sql_str)

    def _get_promo_code(self):
        sql_str = "SELECT promo_code "\
                  "FROM promo_codes LIMIT 1"
        rowcount, results = self._sql.query_sql(sql_str)
        promo_code = results[0][0]
        sql_str = "DELETE FROM promo_codes "\
                  "WHERE promo_code = '{}'".format(promo_code)
        self._sql.exec_sql(sql_str)
        return promo_code

    def _verify_password(self, account_id, password):
        sql_str = "SELECT * "\
                  "FROM accounts "\
                  "WHERE account_id = '{}' "\
                  "AND password = '{}'".format(account_id, password)
        rowcount, results = self._sql.query_sql(sql_str)
        return rowcount

    def _query_bank_card(self, account_id):
        sql_str = "SELECT bank, branch, account, card_no "\
                  "FROM bank_card "\
                  "WHERE account_id = '{}' ".format(account_id)
        return self._sql.query_sql(sql_str)

    def _agent_type(self, flags):
        if flags == 'client':
            return 2
        if flags == 'general_agent':
            return 3
        if flags == 'super_admin':
            return 4
        if flags == 'advanced_agent':
            return 5
        return 0

    def fund_approved(self, voucher_no, form):
        datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_str = "SELECT status "\
                  "FROM vouchers "\
                  "WHERE voucher_no = '{}'".format(voucher_no)
        rowcount, results = self._sql.query_sql(sql_str)
        if not rowcount:
            return {'error': 'invaild voucher_no'}
        if results[0][0] != 1:
            return {'error': 'already approved'}
        status = 2
        if form['active'] == 'reject':
            status = 3
        sql_str = "UPDATE vouchers "\
                  "SET status = {}, remark = '{}' "\
                  "WHERE voucher_no = '{}'".format(status, form['remark'], voucher_no)
        self._sql.exec_sql(sql_str)
        msg = {'voucher_no': voucher_no, 'status': status,
               'datetime': datetime, 'remark': form['remark']}
        self._client.push_message(b'approval_voucher', msg)
        return {'error': ''}

    def login(self, form):
        account = form['account']
        password = form['password']
        sql_str = "SELECT password FROM accounts "\
                  "WHERE account_id = '{}'".format(account)
        rowcount, results = self._sql.query_sql(sql_str)
        if not rowcount or results[0][0] != password:
            return {'error': 'fail'}
        return {'error': 'ok'}

    def register_account(self, form):
        rowcount, results = self._query_accounts(form['id'])
        if rowcount:
            return {'error': 'Exist id'}
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        promo_code = self._get_promo_code()
        agent_id = self._get_agent_id(form['promo_code'])
        sql_str = "INSERT INTO accounts "\
                  "(account_id, password, nickname, full_name, titles, country, "\
                  "province, city, address, phone, birthday, agent_id, status, "\
                  "create_datetime, type, promo_code) "\
                  "VALUES "\
                  "('{}', '{}', '{}', '{}', '{}', '{}', '{}', "\
                  "'{}', '{}', '{}', '{}', '{}', '{}', '{}', 'client', '{}')".format(
                  form['id'], form['password'], form['nickname'],  
                  form['full_name'], form['titles'], form['country'], form['province'], form['city'], 
                  form['address'], form['telephone'], form['birthday'], 
                  agent_id, 'inactive', create_time, promo_code)
        self._sql.exec_sql(sql_str)
        msg = {'account': form['id'], 'password': form['password'], 
                'full_name': form['full_name'], 'agent': agent_id, 
                'telephone': form['telephone'], 'email':'xxx.xxx.com',
                'create_datetime': create_time}
        self._client.push_message(b'register_account', msg)
        return {'error': ''}

    def bind_bank_card(self, account_id, form):
        rowcount, results = self._query_accounts(account_id)
        if not rowcount:
            return {'error': 'Invalid id'}
        rowcount, results = self._query_bank_card(account_id)
        if rowcount:
            return {'error': 'Is bind bank_card'}
        sql_str = "INSERT INTO bank_card "\
                  "(account_id, bank, branch, account, card_no) "\
                  "VALUES "\
                  "('{}', '{}', '{}', '{}', '{}')".format(
                  account_id, form['bank'], form['branch'],
                  form['account'], form['card_no'])
        self._sql.exec_sql(sql_str)
        return {'error': ''}

    def get_account_info(self, account_id):
        a_rowcount, a_results = self._query_accounts(account_id)
        b_rowcount, b_results = self._query_bank_card(account_id)
        if not a_rowcount:
            return {'error': 'invalid id'}

        basic = {'full_name':'', 'birthday':'', 'country':'',
                'province':'', 'city':'', 'telephone':'', 'promo_code':''}
        bank_card = {'bank':'', 'branch':'', 'account':'', 'card_no':''}
        account_type = ''
        if a_rowcount:
            result = a_results[0]
            basic['full_name'] = result[0]
            basic['birthday'] = result[1]
            basic['country'] = result[2]
            basic['province'] = result[3]
            basic['city'] = result[4]
            basic['telephone'] = result[5]
            basic['promo_code'] = result[7]
            account_type = result[6]
        if b_rowcount:
            result = a_results[0]
            bank_card['bank'] = result[0]
            bank_card['branch'] = result[1]
            bank_card['account'] = result[2]
            bank_card['card_no'] = result[3]
        return {'basic':basic, 'type': account_type, 'bank_card':bank_card}

    def get_account_balance(self, account_id):
        a_rowcount, a_results = self._query_accounts(account_id)
        if not a_rowcount:
            return {'error': 'invalid id'}
        result = self._client.request(b'account_balance', {'account': account_id})
        return result

    
    def reset_password(self, account_id, form):
        if not self._verify_password(account_id, form['old_password']):
            return {'error': 'Invalid password'}
        sql_str = "UPDATE accounts "\
                  "SET password = '{new_password}' "\
                  "WHERE account_id = '{account_id}'".format(account_id=account_id, 
                  new_password=form['new_password'])
        self._sql.exec_sql(sql_str)
        msg = {'account': account_id, 'password': form['new_password']}
        self._client.push_message(b'reset_password', msg)
        return {'error': ''}

    def create_voucher(self, account_id, form):
        method_flags = 2
        if form['method'] == 'deposit':
            method_flags = 1
        voucher_no = "C%s%04d" % (time.strftime("%Y%m%d%H%M", time.localtime()),
                                 self._last_voucher_no)
        self._last_voucher_no = (self._last_voucher_no + 1) % 10000
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql_str = "INSERT INTO vouchers "\
                  "(account_id, voucher_no, amount, deposit, create_datetime, status) "\
                  "VALUES "\
                  "('{}', '{}', '{}', {}, '{}', 1)".format(
                  account_id, voucher_no, form['value'], method_flags, create_time)
        self._sql.exec_sql(sql_str)
        msg = {'account': account_id, 'voucher_no': str(voucher_no), 
                'amount': form['value'], 'deposit': method_flags, 'channel': form['channel'], 
                'status': 1, 'create_datetime': create_time}
        self._client.push_message(b'create_voucher', msg)
        return {'voucher_no': str(voucher_no)}

    def get_agent_info(self, account_id, form):
        rowcount, results = self._get_agent_info(account_id)
        data = []
        for result in results:
            item = {'id': result[0], 'is_live': True, 'agent': result[1], 
                    'create_datetime': result[2], 'status': result[3]}
            data.append(item)
        return {'row_size': rowcount, 'data': data}

    def create_agents(self, form):
        agent_type = self._agent_type(form['type'])
        if not agent_type:
            return {'error': 'invalid type'}
        rowcount, results = self._query_accounts(form['id'])
        if not rowcount:
            return {'error': 'invalid id'}
        sql_str = "UPDATE accounts "\
                  "SET type = '{}' "\
                  "WHERE account_id = '{}'".format(form['type'], form['id'])
        self._sql.exec_sql(sql_str)
        msg = {'account': form['id'], 'type': agent_type, 'title': 1}
        self._client.push_message(b'active_agent', msg)
        return {'error': ''}

