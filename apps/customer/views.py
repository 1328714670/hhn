from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import  GenericAPIView
from rest_framework.views import APIView
from customer.xu import worker_information_okXu, pwd_updateXu
from user.models import Customer, Worker, User, Order, Finance
from user.utils import address_data


class login_judge(APIView):
    def get(self,req):
        worker_id=req.COOKIES.get('user')
        worker = Worker.objects.get(worker_id=worker_id)
        data = {'worker': worker}
        return render(req, 'worker/worker_information.html', context=data)

    def post(self,req):
        dic_data=address_data(req.data)
        mobile=dic_data ['telephone']
        try:
            # 客户账号
            customer=Customer.objects.get(customer_telephone=mobile)
            data = {'customer':customer}
            resp=render(req, 'customer/customer_information.html',context=data,status=301)
            resp.set_cookie('user',customer.customer_id)
            return resp

        except Customer.DoesNotExist:
            #员工账号
            try:
                worker=Worker.objects.get(worker_telephone=mobile)
                print('员工账号')
                data={'worker':worker}

                resp=render(req, 'worker/worker_information.html',context=data)
                resp.set_cookie('user', worker.worker_id)
                return resp


            except Worker.DoesNotExist:
                #无注册者
                d={'e':'无此用户'}
                return render(req,'login.html',context=d)

class worker_information_ok(GenericAPIView):
    serializer_class = worker_information_okXu
    def get(self,res):
        return redirect(reverse('customer:login_judge'))
    def post(self,req):
        try:
            dict_data=address_data(req.data)

            worker_id=req.COOKIES.get('user')

            worker=Worker.objects.get(worker_id=worker_id)

            xu=self.get_serializer(worker,data=dict_data)

            xu.is_valid(raise_exception=True)

            xu.save()
            return redirect(reverse('customer:login_judge'))

        except:

            worker_id = req.COOKIES.get('user')
            worker = Worker.objects.get(worker_id=worker_id)
            d={'e':xu.errors,'worker':worker}

            return render(req,'worker/worker_information.html',context=d)

class worker_logout(APIView):
    def get(self,request):
        res=redirect(reverse('user:index'))
        res.delete_cookie('user')
        return res

class worker_change_worker_password(GenericAPIView):
    queryset=Worker.objects.all()
    serializer_class = pwd_updateXu
    def get(self,req):
        worker_id = req.COOKIES.get('user')
        worker = Worker.objects.get(worker_id=worker_id)
        d  = {'worker': worker}
        return render(req,'worker/change_worker_password.html',context=d)
    def post(self,req):
        try:
            data=address_data(req.data)
            worker_id = req.COOKIES.get('user')
            W= Worker.objects.get(worker_id=worker_id)
            user=User.objects.get(user_telephone=W.worker_telephone)
            if user.user_password != data['oldPassword']:
                d={'e':'原密码错误！'}
                return render(req, 'worker/change_worker_password.html', context=d)
            print(user)
            xu=self.get_serializer(user,data=data)
            xu.is_valid(raise_exception=True)
            xu.save()
            return redirect(reverse('customer:login_judge'))
        except:
            d={'e':xu.errors}
            return render(req, 'worker/change_worker_password.html', context=d)


class worker_finance_infomation(GenericAPIView):
    def get(self,req):
        worker_pk = req.COOKIES.get('user')

        w_data=Worker.objects.get(worker_id=worker_pk)

        fince_data=Finance.objects.filter(worker=w_data)

        for i in fince_data:
            i.income=0.8 * (i.platform_cost)

        data={'record':w_data,
              'records':fince_data
              }
        return render(req,'worker/finance_infomation.html',context=data)


class finance_infomation(GenericAPIView):
    def get(self, req):
        worker_id = req.COOKIES.get('user')
        orders = Order.objects.filter(worker_id=worker_id)
        data = {
            "records": orders,
            'record':Worker.objects.get(worker_id=worker_id)
        }
        return render(req, 'worker/order_record.html', context=data)




