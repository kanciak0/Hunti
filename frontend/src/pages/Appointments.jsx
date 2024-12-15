import { useState, useEffect } from "react";
import api from "../api.js";

function Appointments() {
    const [appointments, setAppointments] = useState([]);
    const [newAppointment, setNewAppointment] = useState({
        date: "",
        time: "",
        description: "",
    });

    useEffect(() => {
        getAppointments();
    }, []);

    const getAppointments = () => {
        api
            .get("/api/appointments/")
            .then((res) => setAppointments(res.data))
            .catch(() => alert("Failed to fetch appointments"));
    };

    const createAppointment = (e) => {
        e.preventDefault();
        api
            .post("/api/appointments/", newAppointment)
            .then((res) => {
                if (res.status === 201) {
                    alert("Appointment created successfully!");
                    getAppointments();
                } else {
                    alert("Failed to create appointment.");
                }
            })
            .catch((err) => alert(err));
    };

    const deleteAppointment = (id) => {
        api
            .delete(`/api/appointments/${id}/`)
            .then((res) => {
                if (res.status === 204) {
                    alert("Appointment deleted!");
                    getAppointments();
                } else {
                    alert("Failed to delete appointment.");
                }
            })
            .catch((err) => alert(err));
    };

    return (
        <div>
            <h2>Appointments</h2>
            <ul>
                {appointments.map((appointment) => (
                    <li key={appointment.id}>
                        {appointment.date} - {appointment.time}: {appointment.description}{" "}
                        <button onClick={() => deleteAppointment(appointment.id)}>Delete</button>
                    </li>
                ))}
            </ul>
            <h2>Create Appointment</h2>
            <form onSubmit={createAppointment}>
                <label>
                    Date:
                    <input
                        type="date"
                        value={newAppointment.date}
                        onChange={(e) => setNewAppointment({ ...newAppointment, date: e.target.value })}
                    />
                </label>
                <br />
                <label>
                    Time:
                    <input
                        type="time"
                        value={newAppointment.time}
                        onChange={(e) => setNewAppointment({ ...newAppointment, time: e.target.value })}
                    />
                </label>
                <br />
                <label>
                    Description:
                    <textarea
                        value={newAppointment.description}
                        onChange={(e) => setNewAppointment({ ...newAppointment, description: e.target.value })}
                    ></textarea>
                </label>
                <br />
                <button type="submit">Create</button>
            </form>
        </div>
    );
}

export default Appointments;
