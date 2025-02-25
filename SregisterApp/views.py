from django.http import HttpResponse
from django.shortcuts import render
from SregisterApp.models import Student, Course, projectForm  

# Create your views here.

def home(request):
    return render(request, "home.html")

def studentlist(request):
    studentlist = Student.objects.all()
    return render(request, 'studentlist.html', {'student_list': studentlist})

def courselist(request):
    courselist = Course.objects.all()
    return render(request, 'courselist.html', {'course_list': courselist})

def register(request):
    if request.method == "POST":
        sid = request.POST.get("student")
        cid = request.POST.get("course")
        studentobj = Student.objects.get(id=sid)
        courseobj = Course.objects.get(id=cid)
        res = studentobj.courses.filter(id=cid)
        if res:
            resp = "<h1>Student with usn %s has already enrolled for the %s</h1>" % (studentobj.usn, courseobj.courseCode)
            return HttpResponse(resp)
        studentobj.courses.add(courseobj)
        resp = "<h1>Student with usn %s successfully enrolled for the course with sub code %s</h1>" % (studentobj.usn, courseobj.courseCode)
        return HttpResponse(resp)
    else:
        studentlist = Student.objects.all()
        courselist = Course.objects.all()
        return render(request, 'register.html', {'student_list': studentlist, 'course_list': courselist})

def enrolledStudents(request):
    if request.method == "POST":
        cid = request.POST.get("Course")
        courseobj = Course.objects.get(id=cid)
        studentlistobj = courseobj.student_set.all()
        return render(request,'enrolledlist.html', {'course': courseobj, 'student_list': studentlistobj})
    else:
        courselist = Course.objects.all()
        return render(request, 'enrolledlist.html', {'Course_List': courselist})
    
def add_project(request):
    if request.method=="POST":
        form=projectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>Project Data Successfully saved</h1>")
        else:
            return HttpResponse("<h1>Project details not saved</h1>")
    else:
        form=projectForm()
        return render(request, "projectReg.html",{'form':form})

from django.views import generic
class StudentListView(generic.ListView):
    model=Student
    template_name="GenericListViewStudent.html"
class StudentDetailView(generic.DetailView):
    model=Student
    template_name="GenericDetailedViewStudent.html"
    
import csv
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table

def generateCSV(request):
    courses = Course.objects.all()
    resp = HttpResponse(content_type="text/csv")
    resp['Content-Disposition'] = 'attachment; filename=course_data.csv'
    writer = csv.writer(resp)
    writer.writerow(['Course Code', 'Course Name', 'Course Credits'])
    for c in courses:
        writer.writerow([c.courseCode, c.courseName, c.courseCredits])
    return resp

def generatePDF(request):
    courses = Course.objects.all()
    resp = HttpResponse(content_type="application/pdf")
    resp['Content-Disposition'] = 'attachment; filename=course_data.pdf'
    pdf = SimpleDocTemplate(resp, pagesize=letter)
    table_data = [['Course Code', 'Course Name', 'Course Credits']]
    for c in courses:
        table_data.append([c.courseCode, c.courseName, str(c.courseCredits)])
    table = Table(table_data)
    pdf.build([table])
    return resp

def registerAjax(request): 
    if request.method == "POST": 
        sid=request.POST.get("susn") 
        cid=request.POST.get("ccode") 
        studentobj=Student.objects.get(id=sid) 
        courseobj=Course.objects.get(id=cid) 
        res=studentobj.courses.filter(id=cid) 
        if res: 
            return HttpResponse("<h1>Student already enrolled</h1>") 
        studentobj.courses.add(courseobj) 
        return HttpResponse("<h1>Student enrolled successfully</h1>") 
        
    else: 
        studentsobj=Student.objects.all() 
        coursesobj=Course.objects.all() 
         
        return render(request,"courseRegUsingAjax.html",{"students":studentsobj,"courses":coursesobj})

def enrolledStudentsUsingAjax(request):
    if request.method=="POST":
        cid=request.POST.get("cname")
        
        courseobj=Course.objects.get(id=cid)
        studentlistobj=courseobj.student_set.all()
        return render(request,'EnrolledStudentsAjax.html',{'course':courseobj,'student_list':studentlistobj})                                                                                   
    else:
        courselist=Course.objects.all()
        return render(request,'Course_search_ajax.html',{'Course_List':courselist})

