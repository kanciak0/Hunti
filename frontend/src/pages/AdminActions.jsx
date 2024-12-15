import { useState, useEffect } from "react";
import api from "../api.js";

function AdminActions() {
    const [actions, setActions] = useState([]);
    const [newAction, setNewAction] = useState("");

    useEffect(() => {
        getActions();
    }, []);

    const getActions = () => {
        api
            .get("/api/admin-actions/")
            .then((res) => setActions(res.data))
            .catch((err) => alert("Failed to fetch admin actions"));
    };

    const createAction = (e) => {
        e.preventDefault();
        api
            .post("/api/admin-actions/create/", { action: newAction })
            .then((res) => {
                if (res.status === 201) {
                    alert("Admin action created successfully!");
                    getActions();
                } else {
                    alert("Failed to create admin action.");
                }
            })
            .catch((err) => alert(err));
    };

    return (
        <div>
            <h2>Admin Actions</h2>
            <ul>
                {actions.map((action) => (
                    <li key={action.id}>{action.action}</li>
                ))}
            </ul>
            <h2>Create Admin Action</h2>
            <form onSubmit={createAction}>
                <label>
                    Action:
                    <textarea
                        value={newAction}
                        onChange={(e) => setNewAction(e.target.value)}
                    ></textarea>
                </label>
                <br />
                <button type="submit">Create</button>
            </form>
        </div>
    );
}

export default AdminActions;