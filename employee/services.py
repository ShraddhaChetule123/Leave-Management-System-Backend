from urllib import response
from rest_framework import status
from core.models import AuthToken, Users
from leaves.models import LeaveType
from .models import *
from .serializer import *


def onboard(token, data):
    print(data.get('leave_count'))
    try:

        token = AuthToken.objects.get(token=token)
        admin = Users.objects.get(id=token.users_id)
        emp_user = Users.objects.get(username=data.get("username"))
        leave_types = LeaveType.objects.all()    
        empl = Employee(user_id=emp_user, isManager=False, experiance=data.get("experiance"),
                        blood_group=data.get("blood_group"), address=data.get("address"),
                        contact_no=data.get("contactno")
                        , dob=data.get("dob"), marital_status=data.get("marital_status"),
                        dept_id=data.get("department"),
                        rep_manager_id_id=data.get("manager"), total_leaves=21,
                        ctc=int(float(data.get('ctc'))*100000),onborded_by=admin)
        empl.save()
        response = {
            'status': True,
            'code': status.HTTP_201_CREATED,
            'message': 'On-boarding Complete'
        }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Invalid Key'
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Invalid Token'
        }
    except Users.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'User not Found'
        }

    return response


def get_employee(token, isAll=True, id=None):
    # employee = None
    try:
        if AuthToken.objects.filter(token=token):
            token = AuthToken.objects.get(token=token)
            user = Users.objects.get(id=token.users_id)
            if user.user_role.role_id == 2:
                if isAll and id is None:
                    employee = Employee.objects.filter(rep_manager_id_id=user.id).all()
                    employee = EmployeeSerializer(employee, many=True)
                    print(1)
                elif isAll == False and id is not None:
                    employee = Employee.objects.filter(eid=id, rep_manager_id_id=user.id).all()
                    employee = EmployeeSerializer(employee)
                    print(2)
                else:
                    employee = None

            elif user.user_role.role_id == 3:
                if isAll == True and id is None:
                    employee = Employee.objects.all()
                    employee = EmployeeSerializer(employee, many=True)
                    print(3)
                elif isAll == False and id is not None:
                    employee = Employee.objects.get(eid=id)
                    employee = EmployeeSerializer(employee)
                else:
                    employee = None
            else:
                employee = None

            if employee is not None:
                response = {
                    'status': len(employee.data) > 0,
                    'code': status.HTTP_200_OK if len(employee.data) > 0 else status.HTTP_404_NOT_FOUND,
                    'message': "Success" if len(employee.data) > 0 else "Not found",
                    'data': employee.data
                }
            else:
                response = {
                    'status': False,
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Dont Have permissions to access this information '
                }
        else:

            response = {
                'status': False,
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Unauthorised user'
            }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Invalid Key'
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorised user'
        }
    except Employee.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Invalid Query'
        }

    return response


def get_manager(token, isAll=True, mid=None):
    try:
        AuthToken.objects.get(token=token)
        if isAll:
            manager = ManagerSerializer(Manager.objects.all(), many=True).data
        else:
            manager = ManagerSerializer(Manager.objects.get(mid=mid)).data

        if manager is not None:
            response = {
                'status': len(manager) > 0,
                'code': status.HTTP_200_OK if len(manager) > 0 else status.HTTP_404_NOT_FOUND,
                'message': "Success" if len(manager) > 0 else "Not found",
                'data': manager
            }
        else:
            response = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Dont Have permissions to access this information '
            }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Invalid Key'
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorised user'
        }
    except Manager.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Invalid Query'
        }
    return response


def update_employee(token, body):
    try:
        token = AuthToken.objects.get(token=token)
        employee = Employee.objects.get(eid=body['eid'])

        if token.users.user_role_id == 2 or token.users.user_role_id == 3 or token.users_id == employee.user_id_id:
            employee = Employee.objects.get(eid=body.get('eid'))

            for (key, value) in body.items():

                if key == 'user_id':
                    if Users.objects.filter(id=value['id']).exists():
                        value = Users.objects.get(id=value['id'])
                        value.fname = body['user_id']['fname']
                        value.lname = body['user_id']['lname']
                        value.save()

                if key == 'rep_manager_id':
                    print(key,value)
                    # break
                    if Manager.objects.filter(mid=value).exists():
                        value = Manager.objects.get(mid=value)

                if key == 'dept':
                    if Department.objects.filter(dept_id=value).exists():
                        value = Department.objects.get(dept_id=value)

                if key == 'onborded_by':
                    if Users.objects.filter(id=value).exists():
                        value = Users.objects.get(id=value)

                setattr(employee, key, value)
            employee.save()

            response = {
                'status': True,
                'code': status.HTTP_201_CREATED,
                'message': 'Updated successfully',
                'data': EmployeeSerializer(employee).data
            }

        else:
            response = {
                'status': False,
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': "You can't do this operation"
            }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Invalid Key'
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorised user'
        }
    except Employee.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorised user'
        }

    return response


def get_department(token, isAll=True, did=None):
    try:
        token = AuthToken.objects.get(token=token)
        if isAll:
            dept = DeptSeriaizer(Department.objects.all(), many=True).data
        else:
            dept = DeptSeriaizer(Department.objects.get(dept_id=did)).data

        if dept is not None:
            response = {
                'status': len(dept) > 0,
                'code': status.HTTP_200_OK if len(dept) > 0 else status.HTTP_404_NOT_FOUND,
                'message': "Success" if len(dept) > 0 else "Not found",
                'data': dept
            }
        else:
            response = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Dont Have permissions to access this information '
            }

    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorized'
        }
    except Department.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Not found'
        }

    return response


def get_hardware(token, id=None):
    try:
        token = AuthToken.objects.get(token=token)
        if id is not None:
            employee = Employee.objects.get(user_id=Users.objects.get(id=id))
        else:
            print(token.users.user_role_id)
            if token.users.user_role_id == 3:
                employee = Employee.objects.all()
            else:
                employee = Employee.objects.get(user_id=token.users)

        if token.users.user_role_id == 3:
            hardware = HardwareDetails.objects.all()
            hardware_data = HardwareSerializer(hardware, many=True).data
        else:
            hardware = HardwareDetails.objects.get(eid=employee)
            hardware_data = HardwareSerializer(hardware).data

        if len(hardware_data) > 0:
            response = {
                'status': True,
                'code': status.HTTP_200_OK,
                'data': hardware_data
            }
        else:
            response = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Not found'
            }
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': "Couldn't accept request"
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Unauthorised'
        }
    except Users.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'User not found for request'
        }
    except Employee.DoesNotExist:
        response = {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'Employee not found'
        }

    return response


def make_manager(token, data):
    try:
        token = AuthToken.objects.get(token=token)
        user = Users.objects.get(id=data['user_id'])
        if Manager.objects.filter(user_id=user).exists():
            response = {
                'status': False,
                'code': status.HTTP_400_BAD_REQUEST,
                'message': f" {user.fname} {user.lname} is already a manager"
            } 
        else:
            manager = Manager(user_id = user)
            manager.save()
            response = {
                'status': True,
                'code': status.HTTP_201_CREATED,
                'message': f" {user.fname} {user.lname} become manager now"
            } 
    except Exception as e:
        response = {
            'status': False,
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        }   
    return response 


def leave_counts(token):
    try:
        token = AuthToken.objects.get(token=token)
        if Employee.objects.filter(user_id=token.users).exists():
            emp = Employee.objects.get(user_id=token.users)
            data = {
                'available': emp.total_leaves,
                'assigned': 21
            }
            response = {
                'status':True,
                'message':'Employee exist with leaves',
                'code':status.HTTP_200_OK,
                'data':data
            }
        else:
            response = {
                'status':True,
                'message':'No Employee',
                'code':status.HTTP_204_NO_CONTENT
            }
    except Exception as e:
        response = {
            'status':False,
            'message':str(e),
            'code':status.HTTP_400_BAD_REQUEST
        }
    return response
