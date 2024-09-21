{
    "name":"Hospital Management System",
    "summary": "helps in managing hospitals",
    "description":""" """,
    "author": "Omar Elasrigy",
    "category": "",
    "version": "17.0.0.1.0",
    "depends" : ['base','crm'],
    "application": True,
    "data":[
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
       'views/patient_view.xml',
        'views/department_view.xml',
        'views/doctor_view.xml',
        'views/customer.xml',
        'report/patient_report.xml'
    ]
}
