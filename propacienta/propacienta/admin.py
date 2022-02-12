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
        c = 0
        c += 1
        ordering["Пациенты"] = c
        c += 1
        ordering["Медицинские карты"] = c
        c += 1
        ordering["Диагнозы"] = c
        c += 1
        ordering["Анализы"] = c
        c += 1
        ordering["Приемы врачей"] = c
        c += 1
        ordering["Назначения врачей"] = c
        c += 1
        ordering["Врачи"] = c
        c += 1
        ordering["Клиники"] = c
        c += 1
        ordering["Медикаменты"] = c
        c += 1
        ordering["Процедуры"] = c

        #app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        app_list = sorted(app_dict.values(), key=lambda x: ordering[x['name']])
        
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list