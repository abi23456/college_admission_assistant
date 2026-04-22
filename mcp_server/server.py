from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("CollegeAdmissionTools")

@mcp.tool()
def get_deadlines(university: str) -> str:
    """Get admission deadlines for a specific university."""
    mock_data = {
        "stanford": "Early Action: Nov 1, Regular Decision: Jan 5",
        "mit": "Early Action: Nov 1, Regular Decision: Jan 4",
        "harvard": "Restrictive Early Action: Nov 1, Regular Decision: Jan 1",
        "uc berkeley": "Regular Decision: Nov 30"
    }
    uni = university.lower()
    if uni in mock_data:
        return f"Deadlines for {university.title()}: {mock_data[uni]}"
    else:
        return f"Sorry, I don't have deadline information for {university}. Please check their official website."

@mcp.tool()
def generate_checklist(applicant_type: str = "freshman") -> str:
    """Generate a step-by-step checklist based on applicant type (freshman, transfer, international)."""
    if applicant_type.lower() == "freshman":
        return """
**Freshman Admission Checklist:**
1. Complete Common App or Coalition App.
2. Submit High School Transcripts.
3. Submit SAT/ACT scores (if not test-optional).
4. Request 2 Letters of Recommendation from teachers.
5. Write and refine Personal Essay.
6. Pay application fee or submit fee waiver.
        """
    elif applicant_type.lower() == "international":
        return """
**International Admission Checklist:**
1. Complete Common Application.
2. Submit translated Transcripts.
3. Provide English Proficiency Test (TOEFL/IELTS/Duolingo).
4. Submit proof of finances (Bank statement/Certification of Finances).
5. Request Letters of Recommendation.
6. Review visa requirements.
        """
    elif applicant_type.lower() == "transfer":
         return """
**Transfer Admission Checklist:**
1. Complete Transfer Application.
2. Submit College Transcripts (and High School if required).
3. Obtain College Report from current institution.
4. Request Academic Evaluation from a college professor.
5. Write transfer-specific essay (Why do you want to transfer?).
        """
    else:
        return "Checklist not found for this applicant type. Please specify freshman, international, or transfer."

@mcp.tool()
def check_eligibility(gpa: float) -> str:
    """Check general eligibility and provide guidance based on GPA."""
    if gpa >= 3.8:
        return "Highly competitive. You are in a strong position for top-tier and selective universities."
    elif gpa >= 3.0:
        return "Eligible. You are competitive for many state and private universities. Focus on strong extracurriculars."
    else:
        return "Consider holistic review schools, community college transfer paths, or targeted regional schools. A strong essay can help!"

if __name__ == "__main__":
    # Run the MCP server over standard I/O (stdio)
    print("Starting College Admission MCP Server over stdio...", flush=True)
    mcp.run(transport='stdio')
