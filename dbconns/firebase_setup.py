from firebase import firebase

class firebee:

    def __init__(self):
        pass

    def fetch_db_members(self):
        try:
            fb = firebase.FirebaseApplication('https://http-service-a672f.firebaseio.com/', None)
        except Exception as e:
            print('Firebase Database connection problems')
            print(str(e))
            pass
        result = fb.get('/dummy_db', None)
        # print result
        firstname = []
        middlename = []
        lastname = []
        dob = []
        birthplace = []

        # keeps the values obtained into a list
        res_list = result.values()
        for ind_list in res_list:
            firstname.append(ind_list['firstname'])
            middlename.append(ind_list['middlename'])
            lastname.append(ind_list['lastname'])
            dob.append(ind_list['dob'])
            birthplace.append(ind_list['birthplace'])

        return firstname, middlename, lastname, dob, birthplace

    def db_member_registration(self, firstname, middlename, lastname, dob, birthplace):
        new_user = {
            'firstname': firstname,
            'middlename': middlename,
            'lastname': lastname,
            'dob':dob,
            'birthplace':birthplace
        }
        try:
            fb = firebase.FirebaseApplication('https://http-service-a672f.firebaseio.com/', None)
        except Exception as e:
            print(str(e))
            print('Firebase connection error')
            pass
        result = fb.post('/dummy_db', data=new_user, params={'print':'pretty'})
        print result
        if result:
            success = True
        else:
            success = False
        return success