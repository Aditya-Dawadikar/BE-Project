from fpdf import FPDF,HTMLMixin
from datetime import date
from PIL import Image


class PDF(FPDF,HTMLMixin):
    
    def get_offset_for_center_string(self,text):
        title_w = self.get_string_width(text)
        doc_w = self.w
        return (doc_w-title_w)/2
    
    def header(self):
        #standard for all reports
        self.set_font('helvetica','',8)
        self.cell(0,7,"This is a report generated from an automated program",ln=True,align='R')
        
    def footer(self):
        # standard for all reports
        self.set_y(-15)
        self.set_font('helvetica','I',10)
        self.cell(0,10,f'Page:{self.page_no()}/{{nb}}',align='C')
        
    def report_info(self,report):
        # report related meta data for report identification in the system
        self.set_font('helvetica','',10)
        self.cell(0,7,"Report id: "+report["id"],ln=True,align='R')
    
    def doctor_info(self,doctor):
        self.set_font('helvetica','B',12)
        self.cell(0,7,"Report By:",ln=True)
        self.set_font('helvetica','',12)
        self.cell(0,7,"Dr. "+doctor["name"],ln=True)
        self.set_font('helvetica','',10)
        self.cell(0,7,doctor["qualification"],ln=True)
        self.cell(0,7,doctor["clinic_address"],ln=True)
        self.cell(0,7,"Clinician id: "+doctor["id"],ln=True)
        self.ln(10)
        
    def patient_info(self,patient):
        self.set_font('helvetica','B',12)
        self.cell(0,7,"Report for:",ln=True)
        self.set_font('helvetica','',12)
        self.cell(0,7,f'Name: {patient["name"]}',align='L',ln=True)
        self.set_font('helvetica','',10)
        self.cell(0,7,f'Age: {patient["age"]}\t\t\t\tSex: {patient["sex"]}\t\t\t\tBlood group: {patient["blood_group"]}',align='L',ln=True)
        self.cell(0,7,f'Patient id: {patient["id"]}',align='L',ln=True)
        self.cell(0,7,f'Contact: {patient["contact"]}',align='L',ln=True)
        self.ln(5)
        
    def report_head(self):
        # Title
        self.set_font('helvetica','B',20)
        self.set_x(self.get_offset_for_center_string(title))
        title_w = self.get_string_width(title)
        self.cell(title_w,10,title,ln=True,align='C')
        
        # date of report
        self.set_font('helvetica','B',10)
        self.cell(0,10,"["+str(date.today())+"]",ln=True,align='C')
        self.ln(10)
        
    def note(self,text):
        # note added by doctor
        self.set_text_color(0,0,0)
        self.set_font('helvetica','',12)
        self.multi_cell(0,5,text)
        self.ln(5)

    def analysis_summary(self,summary):
        # summary table
        self.set_font('helvetica','B',12)
        self.cell(0,10,"Report Summary",ln=True,align='C')
        self.set_font('helvetica','',12)
        self.write_html(f"""
            <section>
                <table width="70%">
                    <tr>
                        <th width="30%">Factor</th>
                        <th width="50%">Value</th>
                        <th width="20%">Probability</th>
                    </tr>
                    <tr>
                        <td>Abnormality </td>
                        <td>{summary["Abnormality"]["name"]}</td> 
                        <td>{summary["Abnormality"]["probability"]}%</td>
                    </tr>
                    <tr>
                        <td>Disorder </td>
                        <td>{summary["Disorder"]["name"]}</td> 
                        <td>{summary["Disorder"]["probability"]}%</td>
                    </tr>
                    <tr>
                        <td>Severity</td>
                        <td>{summary["Severity"]["name"]}</td>
                        <td>{summary["Severity"]["probability"]}%</td>
                    </tr>
                </table>
            </section>                
        """)
    
    def set_image(self,images):
        img1 = Image.open(images["url_1"])
        img1 = img1.resize((150, 150), resample=Image.NEAREST)
        
        img2 = Image.open(images["url_2"])
        img2 = img2.resize((150, 150), resample=Image.NEAREST)
        
        self.image(img1, x=40, y=55)
        self.image(img2, x=120, y=55)
        self.ln(5)
        
    def disorder_table(self,disorder):
        line_height = 7
        col_width = 100
        self.set_font("helvetica",'B',12)
        self.multi_cell(col_width, line_height,"Disorder \t\t\t", ln=3, max_line_height=self.font_size,align='R')
        self.multi_cell(col_width, line_height, "Probability", ln=3, max_line_height=self.font_size,align='L')
        self.ln(line_height)
        
        self.set_font("helvetica",'',12)
        for i,c in enumerate(disorder["classes"]):
            self.multi_cell(col_width, line_height, str(c+":\t\t\t"), ln=3, max_line_height=self.font_size,align='R')
            self.multi_cell(col_width, line_height, str(disorder["probability"][i])+"%", ln=3, max_line_height=self.font_size,align='L')
            self.ln(line_height)
            
        self.ln(10)
            
    def abnormality_table(self,abnormality):
        line_height = 7
        col_width = 100
        self.set_font("helvetica",'B',12)
        self.multi_cell(col_width, line_height,"Abnormality \t\t\t", ln=3, max_line_height=self.font_size,align='R')
        self.multi_cell(col_width, line_height, "Probability", ln=3, max_line_height=self.font_size,align='L')
        self.ln(line_height)
        
        self.set_font("helvetica",'',12)
        for i,c in enumerate(abnormality["classes"]):
            self.multi_cell(col_width, line_height, str(c+":\t\t\t"), ln=3, max_line_height=self.font_size,align='R')
            self.multi_cell(col_width, line_height, str(abnormality["probability"][i])+"%", ln=3, max_line_height=self.font_size,align='L')
            self.ln(line_height)
        
        self.ln(10)
        
    def segment_analysis(self,segment):
        self.ln(20)
        self.set_font('helvetica','',12)
        self.cell(0,10,f"Breathing Cycle: {segment['id']}",ln=True,align='C')
        self.set_font('helvetica','',12)
        self.set_image({"url_1":segment["Images"]["waveform_url"],"url_2":segment["Images"]["spectrogram_url"]})
        self.ln(70)
        self.disorder_table(segment["Disorder"])
        self.abnormality_table(segment["Abnormality"])
        
    def assembler(self,report,doctor,patient,summary,text,segment_list):
        # initializing pdf object for standardization
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True,margin=15)
        self.allow_images_transparency = False

        # report summary page
        self.add_page()
        self.report_info(report)
        self.doctor_info(doctor)
        self.report_head()
        self.patient_info(patient)
        self.note(text)
        self.analysis_summary(summary)

        # analysis page: Analysis visualizations segmentwise analysis
        for segment in segment_list:
            self.add_page()
            self.segment_analysis(segment)
            
    def export(self,report,doctor,patient,summary,text,segment_list,filename):
        self.assembler(report,doctor,patient,summary,text,segment_list)
        self.output(filename)


report={
    "id":"xae12"
}
doctor={
    "name":"Aditya Dawadikar",
    "qualification":"MBBS",
    "clinic_address":"201-A, Uday glorious park, Akurdi",
    "id":"h12r81h7f1o8281fb"
}
patient = {
    "name":"Aditya Dawadikar",
    "age":21,
    "blood_group":"B+",
    "contact":"9850221407",
    "sex":"male",
    "id":"awoblwbqb2fbo881217"
}
summary={
    "Abnormality":{
        "name":"crackle",
        "probability":91
    },
    "Disorder":{
        "name":"pneumonia",
        "probability":83
    },
    "Severity":{
        "name":"moderate manifestation",
        "probability":78
    }
}
segment_list=[{
        "id":"dblawbi7u1271vf218f8129",
        "Images":{
            "waveform_url":"waveform.png",
            "spectrogram_url":"spectrogram.png",
        },
        "Abnormality":{
            "classes":["crackle","wheeze"],
            "probability":[91,32]
        },
        "Disorder":{
            "classes":["pneumoia","asthma","bronchiolitis","healthy","fibrosis"],
            "probability":[67.3,91.87,32.2,0.34,21.3]
        }
    },{
        "id":"dblawbi7u1271vf218f8129",
        "Images":{
            "waveform_url":"waveform.png",
            "spectrogram_url":"spectrogram.png",
        },
        "Abnormality":{
            "classes":["crackle","wheeze"],
            "probability":[91,32]
        },
        "Disorder":{
            "classes":["pneumoia","asthma","bronchiolitis","healthy","fibrosis"],
            "probability":[67.3,91.87,32.2,0.34,21.3]
        }
    },{
        "id":"dblawbi7u1271vf218f8129",
        "Images":{
            "waveform_url":"waveform.png",
            "spectrogram_url":"spectrogram.png",
        },
        "Abnormality":{
            "classes":["crackle","wheeze"],
            "probability":[91,32]
        },
        "Disorder":{
            "classes":["pneumoia","asthma","bronchiolitis","healthy","fibrosis"],
            "probability":[67.3,91.87,32.2,0.34,21.3]
        }
    }
]

title="Medical Report"
meta="This report is generated in a automated way"
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi ac sem ut erat convallis efficitur in sed neque. Pellentesque maximus commodo lectus a luctus. Morbi quis enim velit. Sed posuere felis vel ex viverra vestibulum. Donec pellentesque nibh ac metus condimentum porta. Nam tincidunt, lacus in luctus rutrum, felis dui pellentesque ante, ut molestie tellus odio ultrices purus. Nunc ut semper mi. Nulla consequat semper commodo. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Ut sit amet vehicula nisl. Suspendisse potenti. Aenean tincidunt faucibus ligula, ac mollis ante tincidunt eget. Mauris a mauris finibus, lacinia lectus id, laoreet tellus."

pdf = PDF('P','mm','A4')
pdf.export(report,doctor,patient,summary,text,segment_list,'report.pdf')