"""IMED Booking tool spec."""

from typing import Any, Dict, List
from datetime import timedelta, date
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import requests
import jmespath

unable_to_search_error = "Unable to search clinics."
class BookingToolSpec(BaseToolSpec):
    """
    Specifies tools for booking an appointment at IMED.
    """

    spec_functions = ["get_scans", "get_body_part",
                      "search_clinic_by_body_part", "search_appointments"]

    def get_scans(
        self, scan_name: str
    ) -> List[Any]:
        """
        Retrieve body part identifier and name.

        Args:
            scan_name (str): Name of the scan.
        """

        expression = """
            [*].{
                body_part_id: key, 
                body_part_name: name
            }"""

        try:
            response = requests.get(
                'https://book.i-med.com.au/api/regions/group_exams_extra_light')
            data = response.json()

            found_children = None
            for item in data:
                if scan_name.lower() in item['group']['name'].lower():
                    found_children = self.get_all_body_parts(item['children'])
                    break

            if found_children != None:
                return jmespath.search(expression, found_children)
            return []
        except requests.exceptions.RequestException:
            return "Unable to search body parts."

    def get_all_body_parts(self, children) -> List[Any]:
        found_children = []
        for child in children:
            if len(child['children']) > 0:
                exam_list = self.get_all_body_parts(child['children'])
                found_children.extend(exam_list)
            else:
                found_children.append(child['group'])
        
        return found_children
    
    def get_body_part(self, body_part_name: str, scan: str) -> str:
        """
        Get body part by name and scan.

        Args:
            body_part_name (str): Name of the body part.
            scan (str): Scan name
        """

        expression = """
            [*].{
                body_part_id: slug, 
                body_part_name: name
            }"""

        try:
            response = requests.get(
                'https://book.i-med.com.au/api/regions/group_exams_extra_light')
            data = response.json()

            found_part = []
            for group in data:
                if scan.lower() in group['group']['name'].lower():
                    found_part.extend(group['exams'])
                    exam_list = self.find_exams(group['children'], body_part_name.lower())
                    found_part.extend(exam_list)

                    if len(found_part) > 0:
                        break

            return jmespath.search(expression, found_part)
        except requests.exceptions.RequestException:
            return "Unable to search body parts."
    
    def find_exams(self, children, body_part_id) -> List[Any]:
        found_part = []
        for b_part in children:
            if body_part_id in b_part['group']['name'].lower() or body_part_id in b_part['group']['key'].lower():
                found_part.extend(b_part['exams'])

            if len(b_part['children']) > 0:
                exam_list = self.find_exams(b_part['children'], body_part_id.lower())
                found_part.extend(exam_list)
        
        return found_part

    def search_clinic_by_body_part(
        self, body_part_id: str, clinic_name: str, **load_kwargs: Dict[str, Any]
    ) -> str:
        """
        Search clinic by body part identifier and clinic name.

        Args:
            body_part_id (str): Body part Identifier.
            clinic_name (str): Clinic name.
            region (str): Region name where the clinic is located.
        """

        try:
            expression = """[].{
                clinic_id: id, 
                clinic_name: name, 
                address: address, 
                suburb: suburb,
                phoneNumber: phoneNumber
            }"""

            response = requests.get(
                f'https://book.i-med.com.au/api/clinics/exam/{body_part_id}/location')
            data = response.json()

            # Filter results by case-insensitive comparison
            found_clinics = []
            if clinic_name != None and len(clinic_name.replace(' ', '')) > 0:
                for item in data['clinics']:
                    if clinic_name.lower() in item['name'].lower():
                        found_clinics.append(item)
            else:
                found_clinics = data
                    
            return jmespath.search(expression, found_clinics)
        except requests.exceptions.RequestException:
            return unable_to_search_error

    def search_appointments(
        self, clinic_id: str, body_part_id: str, **load_kwargs: Dict[str, Any]
    ) -> str:
        """
        Search appointments by clinic ID and body part ID.

        Args:
            clinic_id (str): Identifier of the clinic.
            body_part_id (str): Body part identifier.
        """

        try:
            expression = """{
                clinic: {
                    clinic_id: clinic.id, 
                    clinic_name: clinic.name, 
                    address: clinic.address, 
                    suburb: clinic.suburb,
                    phoneNumber: clinic.phoneNumber
                },
                dailyAppointments: dailyAppointments[].{
                    day: @.day,
                    appointments: appointments[].{
                        deviceId: @.deviceId,
                        startDateTime: @.startDateTime, 
                        endDateTime: @.endDateTime
                    }
                }
            }"""

            start_date= date.today()
            end_date= start_date + timedelta(days=7)
            response = requests.get(f'https://book.i-med.com.au/api/exams/{body_part_id}/appointments/clinics?startDate={start_date.strftime("%Y-%m-%d")}&endDate={end_date.strftime("%Y-%m-%d")}&clinicIds={clinic_id}')

            if response.status_code == 200:
                data = response.json()
                return jmespath.search(expression, data[0]['examClinicAppointments'][0]['clinicAppointments'])

        except requests.exceptions.RequestException:
            return unable_to_search_error

    def search_clinic(
        self, clinic_name: str, region: str
    ) -> List[Any]:
        """
        Search clinics by name and region.

        Args:
            clinic_name (str): Clinic name.
            region (str): Region name where the clinic is located.
        """

        try:
            response = requests.get('https://book.i-med.com.au/api/clinics')
            data = response.json()

            # Filter results by case-insensitive comparison
            found_clinics = []
            for item in data:
                if clinic_name.lower() in item['name'].lower():
                    found_clinics.append(item)

            return found_clinics
        except requests.exceptions.RequestException:
            return unable_to_search_error
