"""
Bangladesh administrative divisions and their districts.
Used for the checkout cascade dropdown (REQ-F-CHK-02).
"""

DIVISIONS_DISTRICTS = {
    'Dhaka': [
        'Dhaka', 'Gazipur', 'Narayanganj', 'Narsingdi', 'Manikganj',
        'Munshiganj', 'Rajbari', 'Madaripur', 'Shariatpur', 'Faridpur',
        'Gopalganj', 'Kishoreganj', 'Tangail',
    ],
    'Chittagong': [
        'Chittagong', "Cox's Bazar", 'Comilla', 'Brahmanbaria', 'Chandpur',
        'Lakshmipur', 'Noakhali', 'Feni', 'Khagrachhari', 'Rangamati', 'Bandarban',
    ],
    'Sylhet': ['Sylhet', 'Moulvibazar', 'Habiganj', 'Sunamganj'],
    'Rajshahi': [
        'Rajshahi', 'Bogura', 'Chapai Nawabganj', 'Joypurhat',
        'Naogaon', 'Natore', 'Pabna', 'Sirajganj',
    ],
    'Khulna': [
        'Khulna', 'Bagerhat', 'Chuadanga', 'Jashore', 'Jhenaidah',
        'Kushtia', 'Magura', 'Meherpur', 'Narail', 'Satkhira',
    ],
    'Barisal': [
        'Barisal', 'Barguna', 'Bhola', 'Jhalokati', 'Patuakhali', 'Pirojpur',
    ],
    'Rangpur': [
        'Rangpur', 'Dinajpur', 'Gaibandha', 'Kurigram', 'Lalmonirhat',
        'Nilphamari', 'Panchagarh', 'Thakurgaon',
    ],
    'Mymensingh': ['Mymensingh', 'Jamalpur', 'Netrokona', 'Sherpur'],
}

ALL_DIVISIONS = list(DIVISIONS_DISTRICTS.keys())


def get_districts(division):
    """Return list of districts for a division, or [] if invalid."""
    return DIVISIONS_DISTRICTS.get(division, [])
