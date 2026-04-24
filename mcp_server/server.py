from mcp.server.fastmcp import FastMCP
import os

# 🔥 Allow external hosts (ngrok fix)
os.environ["FASTMCP_ALLOW_ALL_HOSTS"] = "true"

# Create MCP server
mcp = FastMCP("CollegeAdmissionTools")

# ---------------- TOOLS ---------------- #

@mcp.tool()
def get_deadlines(university: str) -> str:
    data = {
        "iit bombay": "JEE Advanced: May, JoSAA Counseling: June-July",
        "iit delhi": "JEE Advanced: May, JoSAA Counseling: June-July",
        "iit madras": "JEE Advanced: May, JoSAA Counseling: June-July",
        "bits pilani": "BITSAT Session 1: May, Session 2: June",
        "nit trichy": "JEE Main: Jan & April, JoSAA Counseling: June",
        "nit surathkal": "JEE Main: Jan & April, JoSAA Counseling: June",
        "delhi university": "CUET UG: May, CSAS Portal Allocation: July",
        "anna university": "TNEA Counseling Registration: May",
        "vit vellore": "VITEEE: April, Counseling: May",
        "srmist": "SRMJEEE: April & June",
        "iisc bangalore": "IISC Portal Registration: June",
        "jadavpur university": "WBJEE: April, Counseling: July",
        "aiims delhi": "NEET UG: May, MCC Counseling: July"
    }
    return data.get(university.lower(), f"No deadline info for {university}")


from typing import Any

@mcp.tool()
def generate_checklist(course_type: Any = "engineering") -> str:
    # Handle the case where the AI sends a JSON object/dict instead of a string
    if isinstance(course_type, dict):
        # Extract the value from the dict, defaulting to "engineering"
        # Sometimes the AI uses the parameter name as the key
        course_type = course_type.get("course_type", "engineering")
        
    course_type = str(course_type).lower()

    if course_type == "engineering":
        return "Engineering: 12th Marksheet, JEE Scorecard, Aadhar, Category Certificate."
    elif course_type == "medical":
        return "Medical: 12th PCB, NEET Scorecard, Medical Certificate."
    elif course_type == "degree":
        return "Degree: 12th Marksheet, CUET Scorecard, TC, Photos."
    else:
        return "Type must be: engineering / medical / degree"


@mcp.tool()
def check_eligibility(twelfth_percentage: str) -> str:
    try:
        val = float(twelfth_percentage)
    except ValueError:
        return "Error: percentage must be a number"
        
    if val >= 90:
        return "Top tier colleges possible"
    elif val >= 75:
        return "Good for NITs / BITS"
    elif val >= 60:
        return "Eligible for many private colleges"
    else:
        return "Consider diploma or improvement"


# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    print(" MCP Server running on port 8000...", flush=True)

    mcp.run(
        transport="sse"
    )