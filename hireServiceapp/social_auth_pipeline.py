from hireServiceapp.models import Customer, Driver

def create_user_by_type(backend, user, request, response, *args, **kwargs):
    # if backend is fb then login with fb
    if backend.name == 'facebook':
        avatar = 'https://graph.facebook.com/%s/picture?type=large' % response['id']

    # if user type is driver and driver object is not exist in db yet then create a new
    # driver object in db with user id = user.id that we got from create_user_by_type(args)
    # otherwise if user_type is not driver then create new customer (and also
    # check if customer does not yet exist in db based on user id)
    if request['user_type'] == "driver" and not Driver.objects.filter(user_id=user.id):
        Driver.objects.create(user_id=user.id, avatar = avatar)
    elif not Customer.objects.filter(user_id=user.id):
        Customer.objects.create(user_id=user.id, avatar = avatar)
