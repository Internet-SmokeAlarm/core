from dependencies.python.fmlaas.model import Project, ProjectPrivilegeTypesEnum

from .abstract_model_testcase import AbstractModelTestCase


class ProjectTestCase(AbstractModelTestCase):

    def test_add_device_pass(self):
        project, _ = self._create_project("1")
        device = self._create_device("1")

        project.add_device(device)

        self.assertTrue(device.id in project.devices)

    def test_to_json_pass(self):
        project, json_repr = self._create_project("1")

        self.assertEqual(project.to_json(), json_repr)

    def test_from_json_pass(self):
        project, json_repr = self._create_project("1")

        self.assertEqual(project, Project.from_json(json_repr))

    def test_get_device_list_pass(self):
        project, _ = self._create_project("1")

        self.assertEqual(0, len(project.get_device_list()))

        device = self._create_device("12311213")
        project.add_device(device)
        device_2 = self._create_device("6768564345")
        project.add_device(device_2)

        self.assertEqual(2, len(project.get_device_list()))
        self.assertTrue(device.id in project.get_device_list())
        self.assertTrue(device_2.id in project.get_device_list())

    def test_is_member_pass(self):
        project, _ = self._create_project("1")
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue(project.is_member("user_12344"))
        self.assertFalse(project.is_member("user_123456"))

    def test_add_or_update_member_pass(self):
        project, _ = self._create_project("1")

        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue("user_12344" in project.members)

    def test_does_member_have_auth_pass(self):
        project, _ = self._create_project("1")
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.ADMIN)

        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.ADMIN))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_ONLY))

    def test_does_member_have_auth_pass_2(self):
        project, _ = self._create_project("1")
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_WRITE)

        self.assertFalse(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.ADMIN))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_ONLY))

    def test_does_member_have_auth_pass_3(self):
        project, _ = self._create_project("1")
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        self.assertFalse(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.ADMIN))
        self.assertFalse(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_WRITE))
        self.assertTrue(
            project.does_member_have_auth(
                "user_12344",
                ProjectPrivilegeTypesEnum.READ_ONLY))

    def test_get_member_auth_level_pass(self):
        project, _ = self._create_project("1")
        project.add_or_update_member(
            "user_12344", ProjectPrivilegeTypesEnum.READ_ONLY)

        self.assertEqual(
            ProjectPrivilegeTypesEnum.READ_ONLY,
            project.get_member_auth_level("user_12344"))

    def test_contains_device_pass(self):
        project, _ = self._create_project("1")

        self.assertFalse(project.contains_device("userser123123"))

        project.add_device(self._create_device("sfksdsf"))

        self.assertTrue(project.contains_device("sfksdsf"))
        self.assertFalse(project.contains_device("123123141"))

    def test_equals_simple_pass(self):
        project_1, _ = self._create_project("1")
        project_2, _ = self._create_project("2")
        project_3, _ = self._create_project("1")

        self.assertEqual(project_1, project_3)
        self.assertNotEqual(project_1, project_2)
        self.assertNotEqual(project_2, project_3)

    def test_equals_hard_pass(self):
        project_1, _ = self._create_project("1")
        project_3, _ = self._create_project("1")

        project_1.add_or_update_member(
            "user_1234456", ProjectPrivilegeTypesEnum.OWNER)

        self.assertNotEqual(project_1, project_3)

    def test_add_or_update_experiment_get_pass(self):
        project, _ = self._create_project("1")

        experiment, _ = self._create_experiment("1")
        project.add_or_update_experiment(experiment)

        self.assertEqual(experiment, project.experiments[0])

    def test_contains_job_pass(self):
        project, _ = self._create_project("1")

        experiment, _ = self._create_experiment("1")
        experiment_2, _ = self._create_experiment("2")
        experiment_2._id = "123123123"

        job_1, _ = self._create_job("1")
        job_2, _ = self._create_job("2")
        job_3, _ = self._create_job("3")
        job_4, _ = self._create_job("4")

        experiment.add_or_update_job(job_1)
        experiment.add_or_update_job(job_3)
        experiment_2.add_or_update_job(job_4)

        project.add_or_update_experiment(experiment)
        project.add_or_update_experiment(experiment_2)

        self.assertTrue(project.contains_job(job_1.id))
        self.assertFalse(project.contains_job(job_2.id))
        self.assertTrue(project.contains_job(job_3.id))
        self.assertTrue(project.contains_job(job_4.id))

    def test_get_active_jobs_pass(self):
        project, _ = self._create_project("1")

        experiment, _ = self._create_experiment("1")
        experiment_2, _ = self._create_experiment("2")

        job_1, _ = self._create_job("1")
        job_3, _ = self._create_job("3")
        job_4, _ = self._create_job("4")

        experiment.add_or_update_job(job_1)
        experiment.add_or_update_job(job_3)
        experiment_2.add_or_update_job(job_4)

        experiment.proceed_to_next_job()
        experiment_2.proceed_to_next_job()

        project.add_or_update_experiment(experiment)
        project.add_or_update_experiment(experiment_2)

        self.assertTrue(job_1.id in project.get_active_jobs())
        self.assertTrue(job_4.id in project.get_active_jobs())
        self.assertFalse(job_3.id in project.get_active_jobs())

    def test_get_all_jobs_ids_pass(self):
        project, _ = self._create_project("1")

        for i in range(10):
            experiment, _ = self._create_experiment("123dafasdf34sdfsdf_{}".format(i),
                                                    str(i))

            for j in range(5):
                job, _ = self._create_job("job_test_id_{}_{}".format(i, j))

                experiment.add_or_update_job(job)

            project.add_or_update_experiment(experiment)

        project_job_ids = project.get_all_job_ids()

        self.assertEqual(len(project_job_ids), 50)

    def test_contains_experiment_pass(self):
        project, _ = self._create_project("1")

        for i in range(10):
            experiment, _ = self._create_experiment(str(i))

            project.add_or_update_experiment(experiment)

        self.assertTrue(project.contains_experiment("5"))
        self.assertFalse(project.contains_experiment("50"))
