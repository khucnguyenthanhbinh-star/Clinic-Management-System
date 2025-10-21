class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def login(self, entered_username, entered_password):
        return self.username == entered_username and self.password == entered_password

class Patient(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Patient")
        self.medical_records = []  # Danh sách hồ sơ bệnh án
        self.appointments = []     # Danh sách lịch hẹn
        self.prescriptions = []    # Danh sách đơn thuốc
        self.invoices = []         # Danh sách hóa đơn

    def view_medical_records(self):
        if not self.medical_records:
            print("Không có hồ sơ bệnh án.")
        else:
            for record in self.medical_records:
                print(record)

    def view_appointments(self):
        if not self.appointments:
            print("Không có lịch hẹn.")
        else:
            for appt in self.appointments:
                print(appt)

    def view_prescriptions(self):
        if not self.prescriptions:
            print("Không có đơn thuốc.")
        else:
            for pres in self.prescriptions:
                print(pres)

    def view_invoices(self):
        if not self.invoices:
            print("Không có hóa đơn.")
        else:
            for inv in self.invoices:
                print(inv)

class Doctor(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Doctor")

    def examine_patient(self, patient, diagnosis):
        record = MedicalRecord(diagnosis)
        patient.medical_records.append(record)
        print(f"Đã ghi kết quả khám cho bệnh nhân {patient.username}: {diagnosis}")

    def prescribe_medicine(self, patient, medicine):
        pres = Prescription(medicine)
        patient.prescriptions.append(pres)
        print(f"Đã kê đơn thuốc cho bệnh nhân {patient.username}: {medicine}")

    def schedule_appointment(self, patient, time):
        appt = Appointment(time)
        patient.appointments.append(appt)
        print(f"Đã đặt lịch hẹn cho bệnh nhân {patient.username} lúc {time}")

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "Admin")

    def view_statistics(self, hospital):
        print(f"Tổng bệnh nhân: {len(hospital.patients)}")
        print(f"Tổng bác sĩ: {len(hospital.doctors)}")

    def manage_users(self, hospital):
        print("Quản lý người dùng: (chưa triển khai chi tiết, chỉ in danh sách)")
        print("Bệnh nhân:", [p.username for p in hospital.patients])
        print("Bác sĩ:", [d.username for d in hospital.doctors])

class Appointment:
    def __init__(self, time):
        self.time = time

    def __str__(self):
        return f"Lịch hẹn lúc: {self.time}"

class Prescription:
    def __init__(self, medicine):
        self.medicine = medicine

    def __str__(self):
        return f"Đơn thuốc: {self.medicine}"

class MedicalRecord:
    def __init__(self, diagnosis):
        self.diagnosis = diagnosis

    def __str__(self):
        return f"Hồ sơ: {self.diagnosis}"

class Invoice:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f"Hóa đơn: {self.amount} VND"

class HospitalSystem:
    def __init__(self):
        self.users = {} 
        self.patients = []
        self.doctors = []
        self.admins = []
        self._init_default_users()

    def _init_default_users(self):
        patient1 = Patient("patient1", "pass123")
        doctor1 = Doctor("doctor1", "pass123")
        admin1 = Admin("admin1", "pass123")
        
        self.users["patient1"] = patient1
        self.users["doctor1"] = doctor1
        self.users["admin1"] = admin1
        
        self.patients.append(patient1)
        self.doctors.append(doctor1)
        self.admins.append(admin1)

    def login(self):
        username = input("Nhập username: ")
        password = input("Nhập password: ")
        if username in self.users and self.users[username].login(username, password):
            print(f"Đăng nhập thành công với vai trò {self.users[username].role}")
            return self.users[username]
        else:
            print("Đăng nhập thất bại.")
            return None

    def run(self):
        while True:
            user = self.login()
            if user:
                if user.role == "Patient":
                    self.patient_menu(user)
                elif user.role == "Doctor":
                    self.doctor_menu(user)
                elif user.role == "Admin":
                    self.admin_menu(user)
            else:
                retry = input("Thử lại? (y/n): ")
                if retry.lower() != 'y':
                    break

    def patient_menu(self, patient):
        while True:
            print("\nMenu Bệnh nhân:")
            print("1. Xem hồ sơ bệnh án")
            print("2. Xem lịch hẹn")
            print("3. Xem đơn thuốc")
            print("4. Xem hóa đơn")
            print("5. Đăng xuất")
            choice = input("Chọn: ")
            if choice == '1':
                patient.view_medical_records()
            elif choice == '2':
                patient.view_appointments()
            elif choice == '3':
                patient.view_prescriptions()
            elif choice == '4':
                patient.view_invoices()
            elif choice == '5':
                break
            else:
                print("Lựa chọn không hợp lệ.")

    def doctor_menu(self, doctor):
        while True:
            print("\nMenu Bác sĩ:")
            print("1. Khám bệnh cho bệnh nhân")
            print("2. Kê đơn thuốc")
            print("3. Đặt lịch hẹn")
            print("4. Đăng xuất")
            choice = input("Chọn: ")
            if choice in ['1', '2', '3']:
                patient_username = input("Nhập username bệnh nhân: ")
                patient = self.users.get(patient_username)
                if patient and isinstance(patient, Patient):
                    if choice == '1':
                        diagnosis = input("Nhập kết quả khám: ")
                        doctor.examine_patient(patient, diagnosis)
                    elif choice == '2':
                        medicine = input("Nhập đơn thuốc: ")
                        doctor.prescribe_medicine(patient, medicine)
                        invoice = Invoice(1000000)  
                        patient.invoices.append(invoice)
                        print("Đã tạo hóa đơn.")
                    elif choice == '3':
                        time = input("Nhập thời gian hẹn: ")
                        doctor.schedule_appointment(patient, time)
                else:
                    print("Bệnh nhân không tồn tại.")
            elif choice == '4':
                break
            else:
                print("Lựa chọn không hợp lệ.")

    def admin_menu(self, admin):
        while True:
            print("\nMenu Quản trị viên:")
            print("1. Xem dữ liệu thống kê")
            print("2. Quản lý người dùng")
            print("3. Đăng xuất")
            choice = input("Chọn: ")
            if choice == '1':
                admin.view_statistics(self)
            elif choice == '2':
                admin.manage_users(self)
            elif choice == '3':
                break
            else:
                print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    system = HospitalSystem()
    system.run()