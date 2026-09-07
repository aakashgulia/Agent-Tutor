\# Agent Tutor



\## Project Overview



Agent Tutor is an AI-based tutor developed for the course \*\*Designing Corporate-Startup Synergies (ENT 3805)\*\*.



The system helps students interact with course material through a conversational AI interface. It uses \*\*Retrieval-Augmented Generation (RAG)\*\* so that answers can be grounded in the project's knowledge base rather than relying only on the language model's general knowledge.



The project uses \*\*Panasonic India / Panasonic Ignition\*\* as the main corporate context for startup-related research.



\---



\## Main Features



\### 1. AI Chat



Students can ask questions about the course and project material.



The system:



1\. Converts the question into an embedding.

2\. Searches the knowledge base for relevant information.

3\. Retrieves the most relevant chunks.

4\. Provides the retrieved information to the LLM.

5\. Generates a grounded answer.

6\. Displays the retrieved sources and similarity scores.



\### 2. Class Reflection



Students can enter:



\- Key points from a class

\- One open or unanswered question



Agent Tutor uses the available course material to generate a concise reflection while keeping the student's notes as the basis.



\### 3. Fortnightly Corporate-Startup News



The system retrieves recent news related to:



\- Panasonic India

\- Panasonic Ignition

\- Panasonic Co.lab

\- Panasonic startup collaboration



Relevant articles are displayed with their source, publication date and original link.



AI-generated interpretations are clearly labelled as interpretations and are not presented as verified facts.



\### 4. Prompt Log



The system stores:



\- Student prompt

\- AI response

\- Student-added notes



This creates a record of the interaction and allows students to add their own observations or corrections.



\### 5. Knowledge Base



The knowledge base contains different types of project information, including:



\- Course material

\- Class topics

\- Readings

\- Panasonic research

\- Group research space



The current knowledge base includes material related to Open Innovation and corporate-startup collaboration.



\---



\## RAG Architecture



The main question-answering flow is:



```text

Student

&#x20;  |

&#x20;  v

Streamlit Web Interface

&#x20;  |

&#x20;  v

Agent Tutor

&#x20;  |

&#x20;  v

Question Embedding

&#x20;  |

&#x20;  v

Knowledge Base Retrieval

&#x20;  |

&#x20;  v

Relevant Course / Project Material

&#x20;  |

&#x20;  v

Llama 3.2 3B

&#x20;  |

&#x20;  v

Grounded Answer

&#x20;  |

&#x20;  +----> Sources / Similarity Scores

