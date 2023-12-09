from .models import MSRProject, MSRField    # , Departments, Employees

from rest_framework import serializers


class MSRProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = MSRProject
        # fields = ('file', 'uploaded_at')   # specific data
        fields = '__all__'


class MSRFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = MSRField
        # fields = ('file', 'uploaded_at')   # specific data
        fields = '__all__'



"""
Tests
"""
# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Departments
#         fields=('DepartmentId','DepartmentName')
#
# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Employees
#         fields=('EmployeeId','EmployeeName','Department','DateOfJoining','PhotoFileName')