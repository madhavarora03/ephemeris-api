from datetime import datetime, timezone

import swisseph as swe

if __name__ == "__main__":
    swe.set_ephe_path("./ephe")
    now = datetime.now(timezone.utc)

    jd_ut, jd_tt = swe.utc_to_jd(
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second + now.microsecond / 1000000.0,
    )

    coords, flags, _ = swe.calc_ut(jd_tt, swe.SUN)
    longitude = coords[0]
    print(f"Sun longitude: {longitude}")
