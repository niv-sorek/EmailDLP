from datetime import date

from src.models.UserComponent import UserComponent


class User:
    def __init__(self, user_id, suspicious, permissions="H"):
        self.user_id = user_id
        self.suspicious = suspicious
        self.permissions = permissions  # permissions
        self.user_components = []

    def reprJSON(self):
        return dict(id=self.user_id,
                    suspicious=self.suspicious,
                    permissions=self.permissions,
                    user_components=self.user_components,
                    level=self.get_user_vulnerability_level())

    def add_component(self, component, update):
        """
        :param component: the Component to add to this User
        :param update: update time
        """
        self.user_components.append(UserComponent(component, update, self))

    def set_update_time(self, component, update):
        """
        Set the UserComponent update time
        """
        for uc in self.user_components:
            if uc.component.__eq__(component):
                uc.update = update

    def set_update_now(self, component):
        """
        Set the UserComponent update time to NOW
        """
        self.set_update_time(component, date.today())

    def get_max_component_level(self):
        return max(user_component.get_risk_level() for user_component in self.user_components)

    def get_user_vulnerability_level(self):
        """
        :return: Number [0-10] represents the USER RISK LEVEL by his riskiest component and his permission
        """
        if self.suspicious:
            return 10.0
        else:
            return self.get_max_component_level()
