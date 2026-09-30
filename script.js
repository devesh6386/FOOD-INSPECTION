// ==========================================
// 1. Navigation & Tab Switching
// ==========================================
function switchTab(targetId) {
    // Hide all content sections
    const allSections = document.querySelectorAll('.section, .content-section');
    allSections.forEach(section => {
        section.classList.remove('active', 'active-section');
    });

    // Remove the blue highlight from all sidebar items
    const allNavItems = document.querySelectorAll('.nav-item');
    allNavItems.forEach(item => {
        item.classList.remove('active');
    });

    // Show the target content section
    const activeSection = document.getElementById(targetId) || document.getElementById('section-' + targetId);
    if (activeSection) {
        activeSection.classList.add('active', 'active-section');
    }

    // Add the blue highlight to the clicked sidebar item
    const activeNavItem = document.getElementById('nav-' + targetId);
    if (activeNavItem) {
        activeNavItem.classList.add('active');
    }
}

// ==========================================
// 2. Authentication & Page Load
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
        // If no token exists, kick them back to the login screen
        window.location.href = "/"; 
    } else {
        // Decode token to show Admin/Inspector ID on the sidebar
        try {
            const payload = JSON.parse(atob(token.split('.')[1]));
            const adminDisplay = document.getElementById("admin-id-display");
            if (adminDisplay) adminDisplay.innerText = payload.sub;
        } catch(e) {
            console.error("Token decode error");
        }
        
        // Auto-load the Scan Repository table if it exists on the page
        fetchYOLOScans();
    }
});

function handleSignOut() {
    localStorage.removeItem("access_token");
    window.location.href = "/";
}

// ==========================================
// 3. YOLO AI Scanning Pipeline
// ==========================================
async function runAIscan() {
    const fileInput = document.getElementById('imageInput'); // Input field for packaging images
    if (!fileInput || fileInput.files.length === 0) {
        alert("Please select at least one image.");
        return;
    }

    const formData = new FormData();
    for(let i = 0; i < fileInput.files.length; i++){
        formData.append("images", fileInput.files[i]);
    }

    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch('/api/analyze-scan', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.status === "success") {
            const details = data.extracted_details;
            
            // Helper function to safely update UI fields if they exist
            const updateField = (id, value) => {
                const el = document.getElementById(id);
                if (el) el.value = value || "N/A";
            };

            updateField('brand_name', details.brand);
            updateField('mrp', details.mrp);
            updateField('mfg_exp_date', details.dates);
            updateField('net_quantity', details.weight);
            updateField('manufacturer', details.manufacturer);
            updateField('fssai_license', details.fssai);
            
            alert("Scan completed and saved to MongoDB.");

            // Update the repository table automatically with the new scan
            fetchYOLOScans();
        } else {
            alert("Analysis failed: " + (data.detail || "Unknown error"));
        }
    } catch(error) {
        console.error("Error running scan:", error);
        alert("Failed to connect to the server.");
    }
}

// ==========================================
// 4. Fetch Scan History for UI Table
// ==========================================
async function fetchYOLOScans() {
    const token = localStorage.getItem("access_token");
    const tbody = document.getElementById("scans-table-body");
    
    // Abort if the table isn't on the current HTML page
    if (!tbody) return; 

    tbody.innerHTML = "<tr><td colspan='5'>Fetching AI data from server...</td></tr>";

    try {
        const response = await fetch("/api/scans", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (response.ok) {
            const scans = await response.json();
            tbody.innerHTML = ""; // Clear loading message
            
            scans.forEach(scan => {
                const details = scan.extracted_details || {};
                let detailsHtml = "";
                for (const [key, value] of Object.entries(details)) {
                    detailsHtml += `<strong>${key}:</strong> ${value} <br>`;
                }

                const statusClass = scan.status === "Compliant" ? "compliant" : "violation";
                const row = `<tr>
                    <td>${scan.scan_id}</td>
                    <td>${scan.inspector_id}</td>
                    <td style="font-size: 0.85rem;">${detailsHtml || "No text detected"}</td>
                    <td><span class="badge ${statusClass}">${scan.status}</span></td>
                    <td>${new Date(scan.timestamp).toLocaleString()}</td>
                </tr>`;
                tbody.insertAdjacentHTML('beforeend', row);
            });
        } else if (response.status === 401) {
            handleSignOut(); // Token expired
        } else {
            tbody.innerHTML = "<tr><td colspan='5'>Error loading scan data.</td></tr>";
        }
    } catch (error) {
        tbody.innerHTML = "<tr><td colspan='5'>Backend server is unreachable.</td></tr>";
        console.error("Fetch error:", error);
    }
}
// ==========================================
// 5. Fetch Officer Requests (Admin Only)
// ==========================================
async function fetchOfficerRequests() {
    const token = localStorage.getItem("access_token");
    const tbody = document.getElementById("requests-table-body");
    
    // Abort if the table isn't on the current HTML page
    if (!tbody) return; 

    tbody.innerHTML = "<tr><td colspan='5'>Fetching pending requests...</td></tr>";

    try {
        const response = await fetch("/api/officer-requests", {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (response.ok) {
            const requests = await response.json();
            
            if (requests.length === 0) {
                tbody.innerHTML = "<tr><td colspan='5'>No pending officer requests at this time.</td></tr>";
                return;
            }

            tbody.innerHTML = ""; // Clear loading message
            
            requests.forEach(req => {
                const row = `<tr>
                    <td><strong>${req.employee_id || 'N/A'}</strong></td>
                    <td>${req.name || 'Unknown Officer'}</td>
                    <td>${req.zone || 'Unassigned'}</td>
                    <td>${new Date(req.created_at || Date.now()).toLocaleDateString()}</td>
                    <td>
                        <button onclick="approveOfficer('${req.employee_id}')" style="background: #28a745; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Approve</button>
                        <button onclick="rejectOfficer('${req.employee_id}')" style="background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">Reject</button>
                    </td>
                </tr>`;
                tbody.insertAdjacentHTML('beforeend', row);
            });
        } else {
            tbody.innerHTML = "<tr><td colspan='5'>Error loading requests data.</td></tr>";
        }
    } catch (error) {
        tbody.innerHTML = "<tr><td colspan='5'>Backend server is unreachable.</td></tr>";
        console.error("Fetch error:", error);
    }
}

// Dummy functions for Approve/Reject buttons
function approveOfficer(empId) {
    alert("Approval API call for " + empId + " would execute here.");
    // You will create a POST/PUT request to your backend here later
}

function rejectOfficer(empId) {
    alert("Rejection API call for " + empId + " would execute here.");
    // You will create a DELETE/PUT request to your backend here later
}