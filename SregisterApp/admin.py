from django.contrib import admin

from SregisterApp.models import Course, Student

# Register your models here.
#admin.site.register(Student)
#admin.site.register(course)
admin.site.site_header='Django App' 
admin.site.site_title='Django App'
@admin.register(Student)
class studentAdmin(admin.ModelAdmin): 
    list_display=('usn','name') 
    ordering=('usn',) 
    search_fields=('name',)
@admin.register(Course)
class courseAdmin(admin.ModelAdmin): 
    list_display=('courseCode','courseName') 
    ordering=('courseCode',) 
    search_fields=('courseName',)