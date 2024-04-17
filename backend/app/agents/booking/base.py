"""IMED Booking tool spec."""

from typing import Any, Dict, List

from llama_index.core.tools.tool_spec.base import BaseToolSpec
import requests
import jmespath


class BookingToolSpec(BaseToolSpec):
    """
    Specifies tools for booking an appointment at IMED.
    """

    spec_functions = ["get_body_parts", "get_body_part_id", "search_clinic", "search_appointments"]

    def get_body_parts(
        self, scan_name: str
    ) -> List[Any]:
        """
        Retrieve body parts of an scan by name.

        Args:
            scan_name (str): Name of the scan.
        """

        expression = """
            [*].{
                body_part_id: group.key, 
                body_part_name: group.name
            }"""
    
        try:
            response = requests.get('https://book.i-med.com.au/api/regions/group_exams_extra_light')
            data= response.json()

            found_group = None
            for item in data:
                if scan_name.lower() in item['group']['name'].lower():
                    found_group = item
                    break

            if found_group != None:
                return jmespath.search(expression, found_group['children'])
            return []
        except requests.exceptions.RequestException:
            return "Unable to search body parts."

    def get_body_part_id(
        self, body_part_id: str, scan: str
    ) -> str:
        """
        Get body part by name and scan.

        Args:
            body_part_id (str): Name of the body identifier.
            scan (str): Scan name
        """

        expression = """
            [*].{
                body_part_id: slug, 
                body_part_name: name
            }"""
    
        try:
            response = requests.get('https://book.i-med.com.au/api/regions/group_exams_extra_light')
            data= response.json()

            found_part= []
            for group in data:
                if scan.lower() in group['group']['name'].lower():
                    found_part.extend(group['exams'])
                    for b_part in group['children']:
                        body_part_id = body_part_id.lower()
                        if body_part_id in b_part['group']['name'].lower() or body_part_id in b_part['group']['key'].lower():
                            found_part.extend(b_part['exams'])
                            for part in b_part['children']:
                                found_part.extend(part['exams'])
                            break
                    if len(found_part) > 0:
                        break

            return jmespath.search(expression, found_part)
        except requests.exceptions.RequestException:
            return "Unable to search body parts."
        
    def search_clinic(
        self, body_part_id: str, clinic_name: str, region: str, **load_kwargs: Dict[str, Any]
    ) -> str:
        """
        Tool to search clinics by body part ID, name and region.

        Args:
            body_part_id (str): Body part ID.
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

            response = requests.get(f'https://book.i-med.com.au/api/clinics/exam/{body_part_id}/location')
            data= response.json()

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
            return "Unable to search clinics."
        
    def search_appointments(
        self, clinic_id: str, body_part_id: str, **load_kwargs: Dict[str, Any]
    ) -> str:
        """
        Tool to search appointments by clinic ID and body part ID.

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

            response = requests.get(f'https://book.i-med.com.au/api/exams/{body_part_id}/appointments/clinics?startDate=2024-04-17&endDate=2024-04-23&clinicIds={clinic_id}')
            
            if response.status_code == 200:
                data= response.json()
                return jmespath.search(expression, data[0]['examClinicAppointments'][0]['clinicAppointments'])
            
        except requests.exceptions.RequestException:
            return "Unable to search clinics."