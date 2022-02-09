from django.contrib import admin

class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """

        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        ordering = {i["name"]:100000 for i in app_dict.values()}
        ordering["Пациенты"] = 1
        ordering["Врачи"] = 2
        #app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        app_list = sorted(app_dict.values(), key=lambda x: ordering[x['name']])
        
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list