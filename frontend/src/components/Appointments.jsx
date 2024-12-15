import { useState, useEffect } from "react";
import api from "../api.js";

function Appointments() {
    const [appointments, setAppointments] = useState([]);
    const [formData, setFormData] = useState({
        relief_recipient: "",
        consultant: "",
        date_time: "",
    });

    useEffect(() => {
        getAppointments();
    }, []);

    const getAppointments = () => {
        api.get("/appointments/")
            .then((res) => setAppointments(res.data))
            .catch(() => alert("Failed to fetch appointments"));
    };

    const createAppointment = (e) => {
        e.preventDefault();
        api.post("/appointments/", formData)
            .then(() => {
                alert("Appointment created successfully!");
                getAppointments();
            })
            .catch(() => alert("Failed to create appointment"));
    };

    return (
        <div>
            <h2>Appointments</h2>
            <ul>
                {appointments.map((appt) => (
                    <li key={appt.id}>
                        {appt.relief_recipient} with {appt.consultant} on{" "}
                        {new Date(appt.date_time).toLocaleString()} - {appt.status}
                    </li>
                ))}
            </ul>
            <h3>Create Appointment</h3>
            <form onSubmit={createAppointment}>
                <label>
                    Relief Recipient ID:
                    <input
                        type="number"
                        value={formData.relief_recipient}
                        onChange={(e) =>
                            setFormData({ ...formData, relief_recipient: e.target.value })
                        }
                    />
                </label>
                <br />
                <label>
                    Consultant ID:
                    <input
                        type="number"
                        value={formData.consultant}
                        onChange={(e) =>
                            setFormData({ ...formData, consultant: e.target.value })
                        }
                    />
                </label>
                <br />
                <label>
                    Date & Time:
                    <input
                        type="datetime-local"
                        value={formData.date_time}
                        onChange={(e) =>
                            setFormData({ ...formData, date_time: e.target.value })
                        }
                    />
                </label>
                <br />
                <button type="submit">Create Appointment</button>
            </form>
        </div>
    );
}

export default Appointments;