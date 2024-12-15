import { useState, useEffect } from "react";
import api from "../api.js";

function AdminActions() {
    const [actions, setActions] = useState([]);
    const [formData, setFormData] = useState({
        user_affected: "",
        action_taken: "",
    });

    useEffect(() => {
        getActions();
    }, []);

    const getActions = () => {
        api.get("/admin-actions/")
            .then((res) => setActions(res.data))
            .catch(() => alert("Failed to fetch actions"));
    };

    const createAction = (e) => {
        e.preventDefault();
        api.post("/admin-actions/create/", formData)
            .then(() => {
                alert("Action created successfully!");
                getActions();
            })
            .catch(() => alert("Failed to create action"));
    };

    return (
        <div>
            <h2>Administrator Actions</h2>
            <ul>
                {actions.map((action) => (
                    <li key={action.id}>
                        {action.administrator} managed {action.user_affected}:{" "}
                        {action.action_taken} on{" "}
                        {new Date(action.action_date).toLocaleString()}
                    </li>
                ))}
            </ul>
            <h3>Create Action</h3>
            <form onSubmit={createAction}>
                <label>
                    User Affected ID:
                    <input
                        type="number"
                        value={formData.user_affected}
                        onChange={(e) =>
                            setFormData({ ...formData, user_affected: e.target.value })
                        }
                    />
                </label>
                <br />
                <label>
                    Action Taken:
                    <input
                        type="text"
                        value={formData.action_taken}
                        onChange={(e) =>
                            setFormData({ ...formData, action_taken: e.target.value })
                        }
                    />
                </label>
                <br />
                <button type="submit">Create Action</button>
            </form>
        </div>
    );
}

export default AdminActions;