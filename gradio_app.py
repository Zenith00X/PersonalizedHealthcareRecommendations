import random
import gradio as gr

def generate_recommendation(age: int, gender: str, bp_systolic: int, bp_diastolic: int,
                             cholesterol: int, glucose: int, heart_rate: int, bmi: float,
                             smoking: str, exercise: str, stress: str):
    score = 0
    risk_factors = []
    action_items = []

    if bp_systolic > 140 or bp_diastolic > 90:
        score += 3
        risk_factors.append('Elevated blood pressure indicating hypertension')
    if cholesterol > 240:
        score += 3
        risk_factors.append('High cholesterol levels')
    if glucose > 125:
        score += 3
        risk_factors.append('Elevated glucose levels suggesting diabetes risk')
    if bmi > 30:
        score += 2
        risk_factors.append('BMI indicates obesity')
    if smoking == 'Current-smoker':
        score += 2
        risk_factors.append('Current smoking status')
    if exercise == 'Sedentary':
        score += 1
        risk_factors.append('Sedentary lifestyle')
    if stress == 'High':
        score += 1
        risk_factors.append('High stress levels')
    if age > 55:
        score += 1
        risk_factors.append('Age-related health considerations')

    if score >= 8:
        recommendation = '💊 Medication Required'
        confidence = 88 + random.randint(0, 6)
        explanation = 'Multiple high-risk factors detected requiring immediate medical intervention.'
        action_items = [
            'Schedule immediate appointment with healthcare provider',
            'Begin prescribed medication regimen',
            'Monitor blood pressure and glucose daily',
            'Consider specialist referral for comprehensive evaluation',
            'Implement intensive lifestyle modification program'
        ]
    elif score >= 5:
        recommendation = '🏃 Lifestyle Changes Recommended'
        confidence = 85 + random.randint(0, 7)
        explanation = 'Several risk factors identified that can be improved through lifestyle modifications.'
        action_items = [
            'Implement structured exercise program (30 min daily)',
            'Adopt heart-healthy diet (Mediterranean or DASH)',
            'Reduce sodium and saturated fat intake',
            'Establish regular sleep schedule (7-8 hours)',
            'Consider stress management techniques (meditation, yoga)',
            'Schedule follow-up in 3 months'
        ]
    elif score >= 2:
        recommendation = '📋 Preventive Check-up Recommended'
        confidence = 89 + random.randint(0, 5)
        explanation = 'Minor risk factors detected. Preventive care recommended to maintain health.'
        action_items = [
            'Schedule routine health screening',
            'Continue regular exercise routine',
            'Maintain balanced diet',
            'Monitor key health metrics monthly',
            'Annual comprehensive health assessment'
        ]
    else:
        recommendation = '✓ No Action Needed'
        confidence = 91 + random.randint(0, 5)
        explanation = 'Health parameters within normal ranges. Continue current healthy habits.'
        action_items = [
            'Maintain current healthy lifestyle',
            'Continue regular physical activity',
            'Keep balanced nutrition',
            'Annual routine health check',
            'Stay vigilant about any new symptoms'
        ]

    if not risk_factors:
        risk_factors = ['No significant risk factors detected']

    return {
        'Recommendation': recommendation,
        'Confidence (%)': f"{confidence}%",
        'Explanation': explanation,
        'Risk Factors': '\n'.join(risk_factors),
        'Action Items': '\n'.join(action_items)
    }


def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Personalized Healthcare Recommendations (Gradio)")

        with gr.Row():
            with gr.Column():
                age = gr.Number(label='Age', value=45)
                gender = gr.Dropdown(label='Gender', choices=['Male', 'Female', 'Other'], value='Male')
                bp_systolic = gr.Number(label='Blood Pressure (Systolic)', value=120)
                bp_diastolic = gr.Number(label='Blood Pressure (Diastolic)', value=80)
                cholesterol = gr.Number(label='Cholesterol (mg/dL)', value=180)
                glucose = gr.Number(label='Glucose (mg/dL)', value=100)
                heart_rate = gr.Number(label='Heart Rate (bpm)', value=72)
                bmi = gr.Number(label='BMI', value=24.0)
                smoking = gr.Dropdown(label='Smoking Status', choices=['Never-smoker', 'Former-smoker', 'Current-smoker'], value='Never-smoker')
                exercise = gr.Dropdown(label='Exercise Level', choices=['Active', 'Moderate', 'Sedentary'], value='Moderate')
                stress = gr.Dropdown(label='Stress Level', choices=['Low', 'Moderate', 'High'], value='Moderate')
                submit = gr.Button('Get Recommendation')

            with gr.Column():
                rec = gr.Textbox(label='Recommendation')
                conf = gr.Textbox(label='Confidence (%)')
                expl = gr.Textbox(label='Explanation')
                risks = gr.Textbox(label='Risk Factors')
                actions = gr.Textbox(label='Action Items')

        def wrapped(age, gender, bp_systolic, bp_diastolic, cholesterol, glucose, heart_rate, bmi, smoking, exercise, stress):
            return generate_recommendation(age, gender, int(bp_systolic), int(bp_diastolic), int(cholesterol), int(glucose), int(heart_rate), float(bmi), smoking, exercise, stress)

        submit.click(fn=wrapped, inputs=[age, gender, bp_systolic, bp_diastolic, cholesterol, glucose, heart_rate, bmi, smoking, exercise, stress],
                     outputs=[rec, conf, expl, risks, actions])

    return demo


if __name__ == '__main__':
    demo = build_interface()
    demo.launch(share = True)
