import { useState, useEffect } from "react";
import api from "../api.js";

function Profile() {
    const [profile, setProfile] = useState({});
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        full_name: "",
        contact_number: "",
        address: "",
    });

    useEffect(() => {
        getProfile();
    }, []);

    const getProfile = () => {
        api.get("/profile/")
            .then((res) => {
                setProfile(res.data);
                setFormData(res.data);
            })
            .catch(() => alert("Failed to fetch profile"));
    };

    const updateProfile = (e) => {
        e.preventDefault();
        api.put("/profile/", formData)
            .then((res) => {
                alert("Profile updated successfully!");
                setProfile(res.data);
                setEditing(false);
            })
            .catch(() => alert("Failed to update profile"));
    };

    return (
        <div>
            <h2>Profile</h2>
            {editing ? (
                <form onSubmit={updateProfile}>
                    <label>
                        Full Name:
                        <input
                            type="text"
                            value={formData.full_name}
                            onChange={(e) =>
                                setFormData({ ...formData, full_name: e.target.value })
                            }
                        />
                    </label>
                    <br />
                    <label>
                        Contact Number:
                        <input
                            type="text"
                            value={formData.contact_number}
                            onChange={(e) =>
                                setFormData({ ...formData, contact_number: e.target.value })
                            }
                        />
                    </label>
                    <br />
                    <label>
                        Address:
                        <textarea
                            value={formData.address}
                            onChange={(e) =>
                                setFormData({ ...formData, address: e.target.value })
                            }
                        ></textarea>
                    </label>
                    <br />
                    <button type="submit">Save</button>
                </form>
            ) : (
                <div>
                    <p>Name: {profile.full_name}</p>
                    <p>Contact Number: {profile.contact_number}</p>
                    <p>Address: {profile.address}</p>
                    <button onClick={() => setEditing(true)}>Edit</button>
                </div>
            )}
        </div>
    );
}

export default Profile;
