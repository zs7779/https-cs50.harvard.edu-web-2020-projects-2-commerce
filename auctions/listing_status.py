STATUS = [
    (0, "Open", "badge-primary"),
    (1, "Closed", "badge-secondary"),
    (2, "Expired", "badge-secondary"),
    (3, "Sold", "badge-info")
]

STATUS_CHOICES = [(s[0], s[1]) for s in STATUS]
STATUS_COLORS = {s[0]: s[2] for s in STATUS}
