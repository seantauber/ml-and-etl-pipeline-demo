# **Audit Report: BPC's Current Infrastructure and Workflows**

## **1. Overview**

This audit assesses BPC's existing capabilities in data acquisition, storage systems, processing workflows, computational resources, and downstream applications related to chemical representation and molecular property prediction. The goal is to identify gaps and requirements for implementing ChemBERTa and integrating its predictions into downstream applications.

---

## **2. Data Acquisition Methods**

### **2.1 Data Sources**

- **Internal Research Data**
  - **Description:** BPC conducts extensive in-house experiments, generating proprietary molecular data from high-throughput screening (HTS), medicinal chemistry efforts, and structure-activity relationship (SAR) studies.
  - **Volume:** Approximately 5 million unique chemical compounds with associated experimental data.
  
- **Public Databases**
  - **Description:** BPC supplements its data with publicly available datasets.
  - **Sources:** PubChem, ChEMBL, DrugBank.
  - **Volume:** Approximately 50 million compounds integrated over the years.

- **Collaborations and Partnerships**
  - **Description:** Data shared through collaborations with academic institutions and biotech firms.
  - **Data Sharing Agreements:** Governed by confidentiality and licensing agreements.

### **2.2 Data Formats**

- **SMILES Strings**
  - **Usage:** Primary format for representing molecular structures.
  - **Applications:** Used in data storage and computational analyses.

- **SDF (Structure Data File)**
  - **Usage:** Contains detailed structural information and associated metadata.
  - **Applications:** Used in cheminformatics tools and for data exchange.

- **InChI Identifiers**
  - **Usage:** Standardized chemical identifiers for interoperability.
  - **Applications:** Facilitating data integration across systems.

### **2.3 Data Acquisition Processes**

- **Automated Data Capture**
  - **Laboratory Information Management Systems (LIMS):** Automates data collection from laboratory instruments.
- **Manual Data Entry**
  - **Limitations:** Potential for human error and inconsistencies.
- **Data Quality Control**
  - **Standard Operating Procedures (SOPs):** Established protocols for data validation and curation.

---

## **3. Data Storage Systems**

### **3.1 Storage Infrastructure**

- **On-Premises Data Centers**
  - **Servers:** High-capacity servers with RAID configurations for redundancy.
  - **Storage Capacity:** Approximately 500 TB of total storage, with 70% utilization.

- **Network-Attached Storage (NAS)**
  - **Usage:** For shared file storage accessible across departments.

### **3.2 Database Systems**

- **Relational Databases**
  - **Oracle Database:**
    - **Usage:** Primary database for structured data, including experimental results and compound metadata.
  - **MySQL Instances:**
    - **Usage:** Used by individual departments for specific applications.

- **Cheminformatics Data Management Systems**

  - **ChemAxon's JChem**
    - **Usage:** Chemical database management, structure searching, and property prediction.
  - **BIOVIA Pipeline Pilot**
    - **Usage:** Data integration and analysis workflows.

### **3.3 Data Backup and Recovery**

- **Backup Solutions**
  - **Tape Backups:** Weekly full backups stored off-site.
  - **Snapshot Backups:** Daily snapshots for critical systems.
- **Disaster Recovery Plan**
  - **Limitations:** Recovery times may be longer than desired for mission-critical applications.

---

## **4. Data Processing Workflows**

### **4.1 Data Preprocessing**

- **Data Cleaning**
  - **Tools:** Open Babel, in-house scripts.
  - **Processes:** Removal of duplicates, standardization of molecular representations.

- **Data Standardization**
  - **Canonical SMILES Conversion**
    - **Purpose:** Ensures consistency in molecular representation.
  - **Normalization**
    - **Processes:** Adjusting pH, tautomeric forms, and stereochemistry.

### **4.2 Feature Extraction**

- **Chemical Fingerprinting**

  - **Traditional Fingerprints:**
    - **Morgan (Circular) Fingerprints:** Radius 2, 1024-bit vectors.
    - **MACCS Keys:** 166-bit structural keys.
  - **Descriptors Calculation:**
    - **Physicochemical Properties:** Molecular weight, logP, hydrogen bond donors/acceptors.

- **Software Tools**

  - **RDKit:**
    - **Usage:** Open-source cheminformatics library for fingerprint generation and descriptor calculation.
  - **KNIME Analytics Platform:**
    - **Usage:** Visual workflow tool for data processing and analysis.

### **4.3 Model Training and Evaluation**

- **Machine Learning Models**

  - **Algorithms Used:**
    - Random Forests, Support Vector Machines (SVMs), Gradient Boosting Machines.
  - **Target Properties:**
    - Biological activity, ADMET properties (Absorption, Distribution, Metabolism, Excretion, Toxicity).

- **Computational Resources**

  - **Local Workstations:**
    - High-performance desktops with multi-core CPUs and 32-64 GB RAM.
  - **Small Compute Cluster:**
    - **Configuration:** 10-node cluster with CPU-only nodes.
    - **Limitations:** Insufficient for large-scale AI/ML workloads requiring GPUs.

### **4.4 Model Deployment**

- **Manual Deployment**

  - **Process:** Models are deployed manually on local servers or shared via file systems.
  - **Limitations:** Lack of automation and scalability.

- **Integration with Applications**

  - **Ad-hoc Integrations:**
    - Models are integrated into specific applications on a case-by-case basis.
  - **Challenges:** Inconsistent integration approaches lead to maintenance difficulties.

---

## **5. Computational Resources**

### **5.1 Hardware**

- **Servers and Workstations**

  - **Specifications:**
    - Multi-core CPUs (Intel Xeon), limited GPU availability (a few NVIDIA GTX 1080 cards for testing).
  - **Storage Systems:**
    - HDD-based storage with some SSDs for high-performance needs.

### **5.2 Software and Tools**

- **Operating Systems**

  - **Linux Servers:** CentOS and Ubuntu for servers.
  - **Windows Workstations:** Used by data scientists and researchers.

- **Programming Languages and Libraries**

  - **Python:** Primary language for data processing and modeling.
  - **R:** Used for statistical analysis and visualization.
  - **Machine Learning Libraries:**
    - scikit-learn, pandas, NumPy.

### **5.3 Limitations**

- **Lack of High-Performance Computing (HPC) Resources**

  - **No Access to GPUs/TPUs at Scale:** Hinders ability to train large AI/ML models.
  - **Limited Parallel Processing Capabilities:** Slows down processing of large datasets.

- **Infrastructure**

  - **Aging Hardware:** Servers nearing end-of-life, leading to performance and reliability issues.
  - **Scalability Constraints:** Infrastructure not designed for scaling up AI/ML workloads.

---

## **6. Downstream Applications and Workflows**

### **6.1 Existing Applications**

- **Drug Discovery Platforms**

  - **In-House Software:** Custom applications for compound library management and virtual screening.
  - **Third-Party Tools:**
    - Schrödinger Suite, MOE (Molecular Operating Environment).

- **Data Visualization and Analysis Tools**

  - **Spotfire, Tableau:** Used for data exploration and visualization.
  - **Jupyter Notebooks:** Employed by data scientists for exploratory analysis.

### **6.2 Integration Points**

- **Data Import/Export**

  - **File-Based Exchanges:** CSV, SDF files moved between systems manually or via scripts.
  - **APIs:** Limited use of APIs for data exchange between applications.

- **Workflow Automation**

  - **ETL Processes:** Custom scripts and scheduled jobs handle data transformation and loading.
  - **Limitations:** Lack of unified workflow management leads to inefficiencies.

### **6.3 Challenges**

- **Data Silos**

  - **Fragmented Systems:** Data spread across multiple databases and file systems with limited integration.
  
- **Inconsistent Data Formats**

  - **Conversion Issues:** Frequent need to convert data formats leads to errors and delays.

- **User Accessibility**

  - **Limited Accessibility:** End-users have difficulty accessing and utilizing models due to technical barriers.

---

## **7. Security and Compliance**

### **7.1 Data Security**

- **Access Controls**

  - **Role-Based Access:** Basic access controls in place but not consistently enforced across all systems.
  
- **Encryption**

  - **Data at Rest:** Limited use of encryption for stored data.
  - **Data in Transit:** SSL/TLS used for some applications, but not universally applied.

### **7.2 Regulatory Compliance**

- **GxP Compliance**

  - **Good Laboratory Practice (GLP):** Procedures in place but not fully integrated with IT systems.
  
- **Data Privacy**

  - **Compliance with GDPR and HIPAA:** Relevant for certain datasets, but policies are not consistently enforced.

---

## **8. Organizational Structure and Skills**

### **8.1 IT and Data Teams**

- **IT Department**

  - **Staffing:** 20 personnel handling infrastructure, networking, and support.
  - **Expertise:** Strong in traditional IT, limited experience with cloud and AI/ML infrastructure.

- **Data Science Team**

  - **Staffing:** 5 data scientists with backgrounds in chemistry and basic machine learning.
  - **Expertise:** Proficient in traditional statistical methods, limited exposure to deep learning and AI/ML at scale.

### **8.2 Skills Gaps**

- **AI/ML Expertise**

  - **Limited Experience with Advanced Models:** Teams are not familiar with transformer architectures or large-scale AI/ML deployments.

- **Cloud Computing**

  - **No Existing Cloud Infrastructure:** Teams lack experience with cloud services like AWS, Azure, or GCP.

- **MLOps Practices**

  - **Absence of MLOps Frameworks:** No standardized processes for model deployment, monitoring, or lifecycle management.

---

## **9. Key Findings and Identified Gaps**

### **9.1 Infrastructure Gaps**

- **Computational Resources**

  - **Insufficient Hardware:** Lack of GPUs and HPC resources required for training transformer models like ChemBERTa.
  
- **Storage Systems**

  - **Scalability Limitations:** Current storage solutions may not handle the increased data volume from new representations and embeddings.

### **9.2 Workflow Inefficiencies**

- **Manual Processes**

  - **High Dependency on Manual Tasks:** Leads to errors and slows down data processing and analysis.

- **Data Integration**

  - **Fragmented Data Ecosystem:** Lack of centralized data management hampers efficiency and collaboration.

### **9.3 Skill and Knowledge Gaps**

- **AI/ML Proficiency**

  - **Training Needs:** Staff require upskilling in deep learning, AI/ML frameworks, and model deployment.

- **Cloud Readiness**

  - **Lack of Cloud Infrastructure:** Requires investment in cloud adoption and associated training.

### **9.4 Downstream Integration Challenges**

- **Limited API Usage**

  - **Integration Difficulties:** Existing applications are not designed to consume AI/ML predictions via APIs.

- **Data Format Incompatibilities**

  - **Need for Standardization:** Inconsistent data formats impede seamless data flow to downstream applications.

### **9.5 Security and Compliance Risks**

- **Inconsistent Security Practices**

  - **Data Protection Concerns:** Potential vulnerabilities due to inconsistent application of security measures.

- **Regulatory Compliance**

  - **Risk of Non-Compliance:** Inadequate integration of compliance requirements into IT systems.

---

## **10. Recommendations for Addressing Gaps**

### **10.1 Infrastructure Upgrades**

- **Invest in HPC Resources**

  - **GPUs and Accelerators:** Acquire hardware or cloud resources suitable for AI/ML workloads.

- **Scalable Storage Solutions**

  - **Data Lakes or Cloud Storage:** Implement scalable storage to handle increased data volume.

### **10.2 Workflow Improvements**

- **Automation**

  - **Adopt Workflow Management Tools:** Use platforms like Apache Airflow or Prefect to automate data pipelines.

- **Data Integration**

  - **Centralized Data Platform:** Establish a unified data platform for better data management and accessibility.

### **10.3 Skill Development**

- **Training Programs**

  - **AI/ML and Cloud Computing:** Provide training and workshops to upskill staff.

- **Hiring**

  - **Recruit Experienced Professionals:** Bring in experts in AI/ML engineering and cloud infrastructure.

### **10.4 Integration Enhancements**

- **API Development**

  - **Implement RESTful APIs:** Facilitate data exchange between systems and applications.

- **Standardize Data Formats**

  - **Data Governance Policies:** Establish standards for data formats and metadata across the organization.

### **10.5 Security and Compliance Strengthening**

- **Enhanced Security Measures**

  - **Implement Encryption and Access Controls:** Apply consistent security practices across all systems.

- **Compliance Integration**

  - **Embed Compliance into IT Processes:** Ensure that regulatory requirements are considered in system designs.

---

## **11. Conclusion**

The audit reveals that while BPC has substantial data assets and basic data processing capabilities, significant gaps exist in infrastructure, workflows, skills, and integration practices. Addressing these gaps is essential for successful implementation of ChemBERTa and the integration of its predictions into downstream applications. The recommendations provided lay the groundwork for the necessary upgrades and changes to achieve BPC's goals.

---

**This audit report provides a comprehensive understanding of BPC's current state, which will inform the subsequent steps in our project plan.**