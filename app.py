from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import google.generativeai as genai
from typing import Dict
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

class JudgmentAnalyzer:
    def __init__(self):
        """Initialize the Google Gemini model with the API key."""
        api_key = os.getenv("API_KEY_1")  # Load API key from environment variable
        genai.configure(api_key=api_key)
        self.model_flash = genai.GenerativeModel("gemini-2.0-flash-exp")

    def analyze_judgment(self, judgment_details: str, crime_details: str, evidence_details: str) -> Dict:
        prompt = f"""
        You are a highly experienced legal expert specializing in the Indian Judiciary System, with a thorough understanding of the Bhartiya Nayay Sanhita (BNS), Indian Penal Code (IPC), and court procedures.Additionally, you have access to authoritative resources like Wikipedia and case law repositories to enhance your analysis. Your task is to analyze and assess a court's judgment based on the provided information.

        ### Guidelines for Analysis:
        1. Read the **Judgment Details**, **Crime Details**, and **Evidence Details** carefully.
        2. **Evaluation Criteria**:
           - **Judgment Validity**:
             - Determine whether the judgment aligns with the principles of justice, evidence presented, and applicable sections of the law.
           - **Judgment Accuracy**:
             - If the judgment is accurate:
               - Provide a clear explanation justifying its correctness.
               - Rate the judgment on a scale of 1-10 based on its alignment with relevant laws and its ability to uphold justice.
             - If the judgment is flawed:
               - Identify the specific aspects where it falls short.
               - Propose an alternative judgment or corrections that better reflect the facts and evidence.
               - Reference specific sections of the BNS, IPC, or other relevant legal precedents.
        3. **Guidance for Parties Involved**:
           - For the **Accused** (if applicable):
             - Suggest strategies to challenge the judgment, including evidence-based arguments and procedural tactics.
             - Recommend legal sections or precedents they can use to build a stronger defense.
           - For the **Petitioner** (case filer):
             - Propose steps to reinforce their case, including additional evidence or arguments that could counter defenses by the accused.
        4. **Legal References**:
           - Use specific references to laws, legal principles, and case precedents to substantiate your analysis.

        ### Key Points to Cover:
        1. Evaluate the logical consistency of the judgment.
        2. Assess the relevance and sufficiency of the evidence presented.
        3. Highlight any gaps in the legal reasoning or adherence to due process.
        4. Offer clear and actionable recommendations for both the accused and the petitioner.
        5. Ensure the tone of your analysis is professional, impartial, and highly detailed.

        ### Input Data:
        - **Judgment Details**: {judgment_details}
        - **Crime Details**: {crime_details}
        - **Evidence Details**: {evidence_details}

        ### Your Task:
        Provide a comprehensive analysis of the judgment. Ensure the response is structured as follows:
        1. **Judgment Validity**:
           - Assessment of correctness.
           - Explanation of reasoning (include legal references).
        2. **Rating** (if judgment is correct):
           - Provide a score with a brief justification.
        3. **Alternative Judgment** (if judgment is incorrect):
           - Proposed judgment and reasoning.
           - Relevant legal sections or precedents.
        4. **Guidance for the Accused**:
           - Clear and actionable steps to challenge the judgment.
        5. **Guidance for the Petitioner**:
           - Suggestions to strengthen their case.
        6. **Conclusion**:
           - Summary of findings and recommendations.

        Provide your analysis in 2048 word with references to the IPC and BNS as required, and conclude with guidance for both the accused and the petitioner.

        """
        try:
            # Generate content using the flash model
            response_flash = self.model_flash.generate_content(prompt)
            flash_text = response_flash.text.strip() if response_flash.text else "No response from flash model."

            # Return the analysis result
            return {"analysis": flash_text}

        except Exception as e:
            return {"error": f"Error in analyzing judgment: {str(e)}"}
        
        
class BNSAdvisor:
    def __init__(self):
        api_key = os.getenv("API_KEY_2")  # Load API key from environment variable
        genai.configure(api_key=api_key)
        self.model_pro = genai.GenerativeModel("gemini-2.0-flash-exp")

    def analyze_crime(self, crime_details: str):
        prompt = f"""
You are an AI legal advisor specializing in the Indian Judiciary System and an expert in the laws introduced under the Bharatiya Nayay Sanhita (BNS), Bharatiya Nagarik Suraksha Sanhita (BNSS), and Bharatiya Sakshya Adhiniyam (BSA), implemented in July 2024. 

Your task is to assist users by analyzing the provided crime details and offering clear, precise legal advice. Follow these steps for accuracy:

1. **Understand Crime Context**:
   - Analyze the crime details thoroughly to identify the core issues.
   - Highlight the key aspects of the crime (e.g., intent, harm caused, evidence, procedural elements).

2. **Identify Relevant BNS Sections**:
   - Determine the **specific sections from the BNS** applicable to the crime.
   - Reference the [BNS and IPC Comparative Table](https://www.thelawadvice.com/articles/comparative-table-of-ipc-and-bharatiya-nyaya-sanhita-2023) to ensure the sections align with the crime's nature.
   - Clearly explain why the identified sections are applicable, including the legal reasoning and applicability of key terminologies.

3. **Map BNS to IPC**:
   - Map the identified BNS sections to their corresponding IPC sections, where possible.
   - Present this mapping clearly to help the user understand the evolution of the laws.

4. **Include BNSS and BSA Sections**:
   - If procedural aspects (e.g., arrest, investigation, trial) are involved, mention the applicable **BNSS sections** (replacing CrPC) using the [BNSS and CrPC Comparative Table](https://www.thelawadvice.com/articles/comparative-table-of-crpc-and-bharatiya-nagarik-suraksha-sanhita-2023).
   - If evidentiary aspects are involved (e.g., admissibility of evidence, burden of proof), mention the applicable **BSA sections** (replacing Indian Evidence Act) using the [BSA and Evidence Act Comparative Table](https://www.thelawadvice.com/articles/comparative-table-of-bharatiya-sakshya-act-2023-and-indian-evidence-act-1872).

5. **Provide Details of Punishments**:
   - Mention the punishments (e.g., imprisonment terms, fines, community service) under the identified BNS sections.
   - Cross-reference the [Bharatiya Nayay Sanhita Wikipedia](https://en.wikipedia.org/wiki/Bharatiya_Nyaya_Sanhita) for accurate information.

6. **Explain in Layperson's Terms**:
   - Simplify complex legal terms and ensure clarity for non-legal users.
   - Structure the explanation into sections for ease of understanding: **Crime Summary**, **Applicable Sections**, **Mapping to IPC**, **Procedural Guidance**, and **Punishments**.

Input:
Crime Details: {crime_details}

Provide a structured, detailed response with:
- A **summary** of the crime.
- The **identified BNS sections** and their explanations.
- Mapping to **IPC sections**, where relevant.
- The applicable **BNSS and BSA sections** for procedural and evidentiary matters.
- The associated **punishments** under the BNS.
- Clear, actionable advice that users can understand and act upon.
"""

        try:
            response_pro = self.model_pro.generate_content(prompt)
            pro_text = response_pro.text.strip() if response_pro.text else "No response from pro model."

            return {"advice": pro_text}

        except Exception as e:
            return {"error": f"Error in analyzing crime: {str(e)}"}

class LegalCaseAnalyzer:
    def __init__(self):
        api_key = os.getenv("API_KEY_3")  # Load API key from environment variable
        genai.configure(api_key=api_key)
        self.model_flash = genai.GenerativeModel("gemini-1.5-flash-002")

    def analyze_case(self, case_description: str) -> Dict:
        prompt = f"""You are a seasoned legal expert tasked with providing an extensive, structured breakdown of arguments for both the plaintiff's and the defendant's advocates in a high level of debate between 2 senior lawyer in high court, and provided section in both ipc and bns . This analysis should be detailed, using legal reasoning suitable for those without legal representation, and should provide insightful guidance.

For 3 round of argument between the plaintiff's and the defendant's advocates, provide the following structured details for each side in atleast 5 points for each structured details, specially for supporting evidence and section and act:

1. **Legal Claims and Defenses**:
   - Outline the primary legal claims, defenses, and rights each side is asserting.
   - Reference relevant acts, laws, and sections that support each argument.
   - Ensure each claim or defense is well-explained to clarify its legal standing.

2. **Supporting Evidence and its Relevance**:
   - List and describe specific types of evidence (e.g., witness testimony, physical evidence, digital records) that support each claim or defense.
   - Explain how each piece of evidence strengthens the advocate's position and its potential impact on the court’s perspective.

3. **Landmark Judgments and Precedents**:
   - Include 5-8 high-profile judgments and legal precedents from similar cases.
   - For each precedent, provide a brief summary and explain its relevance to the current case.
   - Discuss how these judgments support the advocate's argument or establish a relevant legal principle.

4. **Counterarguments and Rebuttals**:
   - Respond directly to the opposing advocate’s points, addressing weaknesses or inconsistencies in their claims.
   - Use legal principles or evidence to counter the other side’s arguments effectively.

5. **Potential Legal Outcomes and Consequences**:
   - Describe the legal consequences and possible outcomes if each side’s arguments are upheld.
   - Discuss both immediate legal implications (e.g., penalties, fines) and long-term consequences (e.g., criminal records, civil liabilities).

Each advocate should respond directly to the previous argument made by the opposing side, attempting to refute or strengthen their case with additional points. Ensure that each round of argument is detailed, precise, and labeled clearly.

Case Description:
{case_description}

Please ensure the analysis is comprehensive and structured, offering a full view of the strengths and weaknesses of each side’s case through a high level of debate between 2 senior lawyer in high court. Present the arguments in a way that is both educational and actionable for someone without legal representation."""

        try:
            # Generate content using the Gemini Flash model
            response_flash = self.model_flash.generate_content(prompt)
            flash_text = response_flash.text.strip() if response_flash.text else "No response from flash model."

            return {
                "success": True,
                "flash_analysis": flash_text
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            

# Initialize analyzers
judgment_analyzer = JudgmentAnalyzer()
bns_advisor = BNSAdvisor()
legal_case_analyzer = LegalCaseAnalyzer()

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return "Welcome To the ChainVerdict ML API"


@app.route('/analyze-judgment', methods=['POST'])
@cross_origin()
def analyze_judgment_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input. JSON data is required."}), 400

        judgment_details = data.get('judgment_details', '')
        crime_details = data.get('crime_details', '')
        evidence_details = data.get('evidence_details', '')

        if not all([judgment_details, crime_details, evidence_details]):
            return jsonify({"error": "Missing required fields: 'judgment_details', 'crime_details', 'evidence_details'"}), 400

        result = judgment_analyzer.analyze_judgment(judgment_details, crime_details, evidence_details)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/bns-advisor', methods=['POST'])
@cross_origin()
def analyze_crime():
    data = request.json
    crime_details = data.get("crime_details", "")

    if not crime_details:
        return jsonify({"error": "Crime details are required"}), 400

    results = bns_advisor.analyze_crime(crime_details)
    return jsonify(results)


@app.route('/legal-advisor', methods=['POST'])
@cross_origin()
def point_analyze_case():
    if not request.is_json:
        return jsonify({"success": False, "error": "Content-Type must be application/json"}), 400

    data = request.get_json()
    case_description = data.get('caseDescription')

    if not case_description:
        return jsonify({"success": False, "error": "Case description is required"}), 400

    result = legal_case_analyzer.analyze_case(case_description)

    if not result.get("success"):
        return jsonify(result), 500

    flash_analysis = result.get("flash_analysis", "No Flash Analysis Found")

    def format_into_points(text: str) -> str:
        lines = text.split('\n')
        formatted_lines = [f"{i+1}. {line.strip()}" for i, line in enumerate(lines) if line.strip()]
        return "\n".join(formatted_lines)

    formatted_flash_points = format_into_points(flash_analysis)

    point_formatted_response = {
        "success": result.get("success"),
        "point_formatted_flash_analysis": formatted_flash_points
    }

    return jsonify(point_formatted_response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)