from audioop import add


class Coach:
    name = 0
    coaches = []
    coach_appontments = []

    def __init__(self, name="", durations=[], working_hours=[]):
        Coach.coaches.append({"name": name, "wh": working_hours, "sd": durations})

    @classmethod
    def getCoaches(cls):
        return cls.coaches

    @classmethod
    def getCoachWorkingHours(cls, name):
        for coach in cls.coaches:
            if coach["name"] == name:
                return coach["wh"]

        return "the coach does not exist"

    @classmethod
    def makeAppointment(cls, coac, tim, duration, appointee):
        coach_found = False
        error = False
        coach_appointments = []
        time_allocated = 0
        can_add = False
        tot = 0
        if len(cls.coach_appontments) > 0:
            for appointment in cls.coach_appontments:
                if appointment["coach"] == coac:
                    coach_found = True
                    coach_appointments.append(appointment)
        for appointment in coach_appointments:
            tot = tot + int(appointment["duration"])

        for appointment in coach_appointments:
            time_allocated = time_allocated + int(appointment["duration"])
            slot = tim.split("-")
            if (
                appointment["time"] == tim
                and duration <= (int(slot[1]) - int(slot[0])) - tot
            ):
                cls.add_new_appointment(
                    coac, tim, duration, appointee, (time_allocated + int(duration))
                )
            else:
                error = True

        if not coach_found:
            cls.add_new_appointment(coac, tim, duration, appointee, duration)
        if error:
            print("the requested time slot is not available")

    @classmethod
    def add_new_appointment(cls, coac, tim, duration, appointee, tot=0):
        allocated = False
        for coach in cls.coaches:
            if coach["name"] == coac:
                for h in coach["wh"]:
                    if h == tim:
                        slot = h.split("-")
                        diff = int(slot[1]) - int(slot[0])
                        if diff >= int(duration):
                            cls.coach_appontments.append(
                                {
                                    "coach": coac,
                                    "time": h,
                                    "appointee": appointee,
                                    "duration": duration,
                                    "available_time": int(diff) - int(tot),
                                }
                            )
                            allocated = True
        if allocated:
            return cls.coach_appontments
        else:
            return "the requested time slot is unavailable"

    @classmethod
    def cancel_appointment(cls, appointee, tim, coach):
        removed = False
        if len(cls.coach_appontments) > 0:
            for appointment in cls.coach_appontments:
                if (
                    appointment["coach"] == coach
                    and appointment["time"] == tim
                    and appointment["appointee"] == appointee
                ):
                    i = cls.coach_appontments.index(appointment)
                    del cls.coach_appontments[i]
                    removed = True
            if removed:
                return "Appointment canceled successfully"
            else:
                return f"There was no appointment made for {appointee} with {coach} at the specified time {tim}"
        else:
            return "No appointments to be canceled"

    @classmethod
    def get_allAppointments(cls):
        return cls.coach_appontments

    @classmethod
    def get_coachappointment(cls, coach):
        c_appointments = []
        for appointment in cls.coach_appontments:
            if appointment["coach"] == coach:
                c_appointments.append(appointment)

        return c_appointments


if __name__ == "__main__":
    coach = Coach("Morris", ["1", "2", "3"], ["7-10", "1-3", "6-10"])
    coach = Coach("Mbae", ["1", "2", "3"], ["7-9", "1-3", "6-10"])

    # print("COACHES================", Coach.getCoaches())
    # print("COACHE WORKING HOURS================", Coach.getCoachWorkingHours("Morris"))

    # make_appointment
    # print("COACHES================", Coach.getCoaches())
    Coach.makeAppointment("Morris", "7-10", 1, "gitonga")
    Coach.makeAppointment("Morris", "7-10", 3, "gg")
    Coach.makeAppointment("Morris", "7-10", 1, "wew")

    # Coach.makeAppointment("Morris", "7-10", 1, "munyua")
    # Coach.makeAppointment("Morris", "7-10", 1, "gg")

    # Coach.makeAppointment("Mbae", "6-10", 2, "prof")

    # Coach.cancel_appointment("munyua", "7-10", "Morris")
    Coach.cancel_appointment("wew", "7-10", "Morris")
    # print(Coach.cancel_appointment("prof", "6-10", "Mbae"))

    # Coach.makeAppointment("Morris", "7-10", 1, "GG")

    print("ALl APPOINTMENTS=====================", Coach.get_allAppointments())
