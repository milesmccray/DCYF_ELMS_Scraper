import requests
import json
from bs4 import BeautifulSoup


# THIS CODE IS WRITTEN HORRIBLY SINCE IT WEB SCRAPES AND I RUSHED, BUT IT WORKS AS OF 11/10/24

class ChildData:
    def __init__(self):
        with open('del_auth.txt', 'r') as f:
            self.del_auth = f.read().strip()

        with open('elms_id.txt', 'r') as f:
            self.elms_ids = f.read().split(',')

        self.cookie = {'DELPortalAuth': self.del_auth}  # Creates the cookie to be sent in request
        self.urls = ['https://apps.dcyf.wa.gov/ELMS/Child/ChildInfo.aspx?ChildId=',
                     'https://apps.dcyf.wa.gov/ELMS/Child/MedicalStatus.aspx?ChildId=',
                     'https://apps.dcyf.wa.gov/ELMS/Child/DentalStatus.aspx?ChildId=',
                     'https://apps.dcyf.wa.gov/ELMS/Child/ECEAPHealthScreenings.aspx?ChildId=',
                     'https://apps.dcyf.wa.gov/ELMS/Child/ChildDevelopment.aspx?ChildId=',
                     'https://apps.dcyf.wa.gov/ELMS/Child/FamilySupport.aspx?ChildId=',
                     'https://apps.dcyf.wa.gov/ELMS/Child/Family/FamilySupport.aspx?ChildId=']

        self.child_data = {}

        self.child_id = None
        self.count = None
        # General
        self.f_name = None
        self.l_name = None
        self.b_date = None
        # Medical Tab
        self.wc_date = None
        self.immunization = None
        # Dental Tab
        self.de_date = None
        # Health Screening Tab
        self.vision_past = None
        self.vision_current = None
        self.vision_referral = None
        self.vision_followup = None
        self.hearing_past = None
        self.hearing_current = None
        self.hearing_referral = None
        self.hearing_followup = None
        # Child Development Tab
        self.asq_date = None
        self.asq_result = None
        self.asq_rescreen = None
        self.asq_date_ee = None
        self.asq_result_ee = None
        self.asq_rescreen_ee = None
        self.ifsp_start = None
        self.ifsp_active = None
        self.ifsp_end = None
        self.iep_start = None
        self.iep_active = None
        self.iep_end = None
        self.pt_dict = {}
        # Family Support Tab
        self.hv_dict = {}
        self.monthly_contact_dict = {}
        # Mobility Tab
        self.pre_assessment = None
        self.post_assessment = None
        self.on_another_child = None
        self.opt_out = None
        self.family_goal = None

    def reset_data(self):
        self.child_id = None
        self.count = None
        # General
        self.f_name = None
        self.l_name = None
        self.b_date = None
        # Medical Tab
        self.wc_date = None
        self.immunization = None
        # Dental Tab
        self.de_date = None
        # Health Screening Tab
        self.vision_past = None
        self.vision_current = None
        self.vision_referral = None
        self.vision_followup = None
        self.hearing_past = None
        self.hearing_current = None
        self.hearing_referral = None
        self.hearing_followup = None
        # Child Development Tab
        self.asq_date = None
        self.asq_result = None
        self.asq_rescreen = None
        self.iep_start = None
        self.iep_active = None
        self.iep_end = None
        self.pt_dict = {}
        # Family Support Tab
        self.hv_dict = {}
        self.monthly_contact_dict = {}
        # Mobility Tab
        self.pre_assessment = None
        self.post_assessment = None
        self.on_another_child = None
        self.opt_out = None
        self.family_goal = None

    def run(self):
        # Run the loop to fetch data
        x = 1
        for child_id in self.elms_ids:
            print(f'child #{x}')
            x += 1
            self.reset_data()
            self.child_id = child_id
            self.count = 0
            for url in self.urls:
                self.count += 1
                self.get_html(url + child_id)

            self.build_child_data2()

    def get_html(self, url):
        raw_html = requests.get(url, cookies=self.cookie)
        if self.count == 1:
            self.household_tab(raw_html.text)
        if self.count == 2:
            self.medical_tab(raw_html.text)
        if self.count == 3:
            self.dental_tab(raw_html.text)
        if self.count == 4:
            self.healthscreening_tab(raw_html.text)
        if self.count == 5:
            self.child_tab(raw_html.text)
        if self.count == 6:
            self.family_tab(raw_html.text)
        if self.count == 7:
            self.mobility_tab(raw_html.text)

    def household_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        try:
            f_name = soup.find('input', {'name': 'ctl00$ctl00$phb$phb$txtFirstName'}).get('value')
            l_name = soup.find('input', {'name': 'ctl00$ctl00$phb$phb$txtLastName'}).get('value')
            birth_date = soup.find('input', {'name': 'ctl00$ctl00$phb$phb$txtBirthDate'}).get('value')

            self.f_name = f_name
            self.l_name = l_name
            self.b_date = birth_date
        except AttributeError:
            print('ERROR: Update del_auth.txt with new cookie || Possibly html changed')
            quit()

    def medical_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

        # WC Date
        wc_date = soup.find('input',
                            {'name': 'ctl00$ctl00$phb$phb$WellChildECEAPUpdateControl1$txtExamDate'}).get('value')
        if wc_date is None:
            try:
                wc_date = soup.find('input', {'id': 'phb_phb_txtWellCheckExam'}).get('value')
            except AttributeError:
                wc_date = 'N/A'

        # Immunization Status
        elms_immu = soup.find('select', {'id': 'phb_phb_ddlImmunizationCurrentStatus'}).find(
            'option', {'selected': 'selected'}).get('value')

        if elms_immu == '1':
            elms_immu = 'Complete'
        if elms_immu == '2':
            elms_immu = 'Exempt'
        if elms_immu == '3':
            elms_immu = 'Conditional'
        if elms_immu == '4':
            elms_immu = 'Out of Compliance - No CIS and IIS data'
        if elms_immu == '5':
            elms_immu = 'Out of Compliance - Child is not complete or Immune'
        if elms_immu == '6':
            elms_immu = 'CIS or IIS not evaluated'
        if elms_immu is None:
            elms_immu = 'N/A'

        self.wc_date = wc_date
        self.immunization = elms_immu

    def dental_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

        # DE Date
        de_date = soup.find('input',
                            {'name': 'ctl00$ctl00$phb$phb$WellChildECEAPUpdateControl1$txtExamDate'}).get('value')
        if de_date is None:
            try:
                de_date = soup.find('span', {'id': 'phb_phb_lblDentalExamLastYear'}).text
            except AttributeError:
                de_date = 'N/A'

        self.de_date = de_date

    def healthscreening_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

        # Vision Date
        self.vision_past = 'N/A'
        self.vision_current = 'N/A'
        self.vision_referral = 'N/A'
        vision_dates = soup.find_all('input', {'class': 'date', 'value': True})
        for line in vision_dates:
            if 'VisionHealthScreening' in str(line):
                if 'disabled' in str(line):
                    self.vision_past = line.get('value')
                if 'ScreeningDate' in str(line):
                    self.vision_current = line.get('value')
                if 'ReferralDate' in str(line):
                    self.vision_referral = line.get('value')

        try:
            self.vision_followup = soup.find('span', {'id': 'phb_phb_visionHeader_lblRequiresFollowUpAnswer'}).text
        except AttributeError:
            self.vision_followup = 'Yes'

        # Hearing Date
        self.hearing_past = 'N/A'
        self.hearing_current = 'N/A'
        self.hearing_referral = 'N/A'

        hearing_dates = soup.find_all('input', {'class': 'date', 'value': True})
        for line in hearing_dates:
            if 'HearingHealthScreening' in str(line):
                if 'disabled' in str(line):
                    self.hearing_past = line.get('value')
                if 'ScreeningDate' in str(line):
                    self.hearing_current = line.get('value')
                if 'ReferralDate' in str(line):
                    self.hearing_referral = line.get('value')
        try:
            self.hearing_followup = soup.find('span', {'id': 'phb_phb_hearingHeader_lblRequiresFollowUpAnswer'}).text
        except AttributeError:
            self.hearing_followup = 'Yes'

    def child_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

        # ASQ
        try:
            raw_asq_info = list(
                soup.find('table', {'id': 'phb_phb_grdDevelopmentalScreening'}).find_all('td', limit=3))
            self.asq_date = raw_asq_info[0].text.strip()
            self.asq_result = raw_asq_info[1].text.strip()
            self.asq_rescreen = raw_asq_info[2].text.strip()

        except (AttributeError, IndexError):
            self.asq_date = 'N/A'
            self.asq_result = 'N/A'
            self.asq_rescreen = 'N/A'

        try:
            raw_asq_info_ee = list(
                soup.find('table', {'id': 'phb_phb_grdEarlyDevelopmentalScreening'}).find_all('td', limit=3))
            self.asq_date_ee = raw_asq_info_ee[0].text.strip()
            self.asq_result_ee = raw_asq_info_ee[1].text.strip()
            self.asq_rescreen_ee = raw_asq_info_ee[2].text.strip()

        except (AttributeError, IndexError):
            self.asq_date_ee = 'N/A'
            self.asq_result_ee = 'N/A'
            self.asq_rescreen_ee = 'N/A'

        # IFSP
        self.ifsp_start = 'N/A'
        self.ifsp_active = 'N/A'
        self.ifsp_end = 'N/A'
        raw_iep_info = list(soup.find('table', {'id': 'phb_phb_grdIFSP'}).find_all('td'))
        if len(raw_iep_info) > 1:
            self.ifsp_start = raw_iep_info[0].text.strip()
            self.ifsp_active = raw_iep_info[2].text.strip()
            self.ifsp_end = raw_iep_info[3].text.strip()

        # IEP
        self.iep_start = 'N/A'
        self.iep_active = 'N/A'
        self.iep_end = 'N/A'

        raw_iep_info = list(soup.find('table', {'id': 'phb_phb_grdIep'}).find_all('td'))
        if len(raw_iep_info) > 1:
            self.iep_start = raw_iep_info[0].text.strip()
            self.iep_active = raw_iep_info[2].text.strip()
            self.iep_end = raw_iep_info[3].text.strip()

        # P/T Conference
        pt_list = []
        raw_pt_info = list(soup.find('table', {'id': 'phb_phb_parentTeachConferences_grdChildMeeting'}).find_all(
            'tr'))
        del raw_pt_info[0]  # Removes dead <tr> tag from html
        for visit in raw_pt_info:
            temp_list = []
            visit = visit.find_all('td')
            temp_list.append(visit[0].text.strip())
            temp_list.append(visit[2].text.strip())
            temp_list.append(visit[5].text.strip())
            pt_list.append(temp_list)

        # Convert List to dictionary
        if len(pt_list) > 0:
            while True:  # Trim list
                if len(pt_list) > 4:
                    del pt_list[-1]
                else:
                    break
            for count, info in enumerate(pt_list, start=1):  # P/T Conference
                self.pt_dict[str(count) + '-PT_Conference'] = {'date': info[0], 'location': info[1], 'description':
                    info[2]}
        else:
            self.pt_dict['1-PT_Conference'] = 'N/A'

    def family_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        family_info = []
        hv_list = []
        monthly_contact_list = []

        # Manipulate Family Support Table Data
        table_data = soup.find('table').find_all('tr')
        for row in table_data:
            notes = list(row.find_all('td'))
            try:
                family_info.append([notes[0].text.strip(), notes[1].text.strip(), notes[2].text.strip(),
                                    notes[3].text.strip(), notes[4].text.strip()])
            except IndexError:
                continue

        # Grabs all monthly contacts that have something in "location" on the table
        for interaction in family_info:
            if interaction[2]:
                hv_list.append(interaction)
            monthly_contact_list.append(interaction[0])

        # Only shows last 4 monthly contacts
        while True:
            if len(monthly_contact_list) > 4:
                del monthly_contact_list[-1:]
            else:
                break

        # Convert List into Dict
        if len(hv_list) > 0:
            while True:  # Trim list
                if len(hv_list) > 4:
                    del hv_list[-1]
                else:
                    break
            for count, info in enumerate(hv_list, start=1):  # Home visits
                self.hv_dict[str(count) + '-HomeVisit'] = {'date': info[0], 'teacher': info[1], 'location': info[2],
                                                           'topic': info[3], 'description': info[4]}
        else:
            self.hv_dict['1-HomeVisit'] = 'N/A'

        if len(monthly_contact_list) > 0:
            for count, date in enumerate(monthly_contact_list, start=1):  # Monthly
                self.monthly_contact_dict[str(count) + '-Monthly'] = date
        else:
            self.monthly_contact_dict['1-Monthly'] = 'N/A'

    def mobility_tab(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')

        # Pre & Post
        if 'Edit 2024-25 Pre Assessment' in soup.text:
            self.pre_assessment = 'Yes'
        else:
            self.pre_assessment = 'No'

        if 'Edit 2024-25 Post Assessment' in soup.text:
            self.post_assessment = 'Yes'
        else:
            self.post_assessment = 'No'

        # Information on another child record
        if soup.find('input', {'id': 'phb_phb_chkDataOnAnotherRecord', 'type': 'checkbox', 'checked': 'checked'}):
            self.on_another_child = soup.find('a', {'id': 'phb_phb_lnkOtherChild'}).text
        else:
            self.on_another_child = 'N/A'

        # Goal Setting Opted Out
        if soup.find('input', {'id': 'phb_phb_chkOptOutGoalSetting', 'type': 'checkbox', 'checked': 'checked'}):
            self.opt_out = 'Yes'
        else:
            self.opt_out = 'No'

        # Family Goal Plans Check
        if soup.find('table', {'id': 'phb_phb_grdGoalsCurrent'}):
            self.family_goal = 'Yes'
        else:
            self.family_goal = 'No'

    def build_child_data2(self):
        self.child_data[f'{self.l_name},{self.f_name}'] = {
            'GENERAL': {'last': self.l_name, 'first': self.f_name, 'birthdate': self.b_date, 'id': self.child_id},
            'EDUCATION': {'IMMUNIZATION': self.immunization,
                          'ASQ': {'asq_date': self.asq_date, 'asq_result': self.asq_result,
                                  'asq_rescreen': self.asq_rescreen, 'asq_date_ee': self.asq_date_ee,
                                  'asq_result_ee': self.asq_result_ee, 'asq_rescreen_ee': self.asq_rescreen_ee},
                          'IFSP': {'ifsp_start': self.ifsp_start, 'ifsp_end': self.ifsp_end,
                                   'ifsp_active': self.ifsp_active},
                          'IEP': {'iep_start': self.iep_start, 'iep_end': self.iep_end,
                                  'iep_active': self.iep_active},
                          'PT_CONFERENCE': self.pt_dict},
            'FAMILY': {'MEDICAL': {'well_child': self.wc_date},
                      'DENTAL': {'dental': self.de_date},
                      'HEALTH_SCREENING': {'VISION': {'past_vision': self.vision_past,
                                                      'current_vision': self.vision_current,
                                                      'referral_vision': self.vision_referral,
                                                      'followup_vision(ref/fail)': self.vision_followup},
                                           'HEARING': {'past_hearing': self.hearing_past,
                                                       'current_hearing': self.hearing_current,
                                                       'referral_hearing': self.hearing_referral,
                                                       'followup_hearing(ref/fail)': self.hearing_followup}},
                      'FAMILY_INFORMATION': {'MONTHLY_CONTACT': self.monthly_contact_dict,
                                             'HOME_VISITS': self.hv_dict},
                      'MOBILITY_INFORMATION': {'pre_assessment': self.pre_assessment,
                                               'post_assessment': self.post_assessment,
                                               'on_another_child': self.on_another_child,
                                               'FAMILY_GOALS': {'opt_out': self.opt_out, 'family_goal':
                                                   self.family_goal}}}}

    def build_child_data(self):
        self.child_data[f'{self.l_name},{self.f_name}'] = {
            'GENERAL': {'last': self.l_name, 'first': self.f_name, 'birthdate': self.b_date, 'id': self.child_id},
            'MEDICAL': {'well_child': self.wc_date, 'immu_status': self.immunization},
            'DENTAL': {'dental': self.de_date},
            'HEALTH_SCREENING': {'VISION': {'past_vision': self.vision_past, 'current_vision': self.vision_current,
                                            'referral_vision': self.vision_referral,
                                            'followup_vision(ref/fail)': self.vision_followup},
                                 'HEARING': {'past_hearing': self.hearing_past,
                                             'current_hearing': self.hearing_current,
                                             'referral_hearing': self.hearing_referral,
                                             'followup_hearing(ref/fail)': self.hearing_followup}},
            'CHILD_DEVELOPMENT': {'ASQ': {'asq_date': self.asq_date, 'asq_result': self.asq_result,
                                          'asq_rescreen': self.asq_rescreen, 'asq_date_ee': self.asq_date_ee,
                                          'asq_result_ee': self.asq_result_ee, 'asq_rescreen_ee': self.asq_rescreen_ee},
                                  'IFSP': {'ifsp_start': self.ifsp_start, 'ifsp_end': self.ifsp_end,
                                          'ifsp_active': self.ifsp_active},
                                  'IEP': {'iep_start': self.iep_start, 'iep_end': self.iep_end,
                                          'iep_active': self.iep_active},
                                  'PT_CONFERENCE': self.pt_dict},
            'FAMILY_INFORMATION': {'HOME_VISITS': self.hv_dict,
                                   'MONTHLY_CONTACT': self.monthly_contact_dict},
            'MOBILITY_INFORMATION': {'pre_assessment': self.pre_assessment, 'post_assessment': self.post_assessment,
                                     'on_another_child': self.on_another_child,
                                     'FAMILY_GOALS': {'opt_out': self.opt_out, 'family_goal': self.family_goal}}}

    def dump(self):
        # Dump final dictionary into JSON
        with open('child_data.json', 'w') as f:
            json.dump(self.child_data, f, indent=4)


if __name__ == "__main__":
    data = ChildData()
    data.run()
    data.dump()
