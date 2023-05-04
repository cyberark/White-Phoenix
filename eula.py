import tkinter as tk

import winreg


def check_key():
    """
    check the registry to see if eula has been accepted
    return: true if accepted, false if not
    """

    EULA_ACCEPTED_REG_KEY = r"SOFTWARE\White Phoenix"
    EULA_ACCEPTED_REG_VALUE = "EULAAccepted"

    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, EULA_ACCEPTED_REG_KEY)
    value_num = winreg.QueryInfoKey(key)
    if value_num[1] != 1:  # check if key has 1 value
        return False
    value = winreg.QueryValueEx(key, EULA_ACCEPTED_REG_VALUE)
    if value[0] != 1:  # check if value is set to 1
        return False
    return True


def create_main_window():
    """
    create the main window for the eula
    return: main window object
    """
    eula_window = tk.Tk()
    eula_window.title("End User License Agreement")
    eula_window.geometry("800x800")
    return eula_window


def create_frames_and_canvas(eula_window):
    """
    initialize the frames and canvas to have the scrollbar match
    return: the 2 frames created
    """

    # create main frame
    frame = tk.Frame(eula_window)
    frame.pack(fill=tk.BOTH, expand=1)

    # create canvas
    canvas = tk.Canvas(frame, height=500)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # add scroll bar to canvas
    eula_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    eula_scrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=eula_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # create second frame
    frame2 = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame2, anchor="nw")

    return frame, frame2


def create_title(eula_text):
    """
    create the eula title
    """
    EULA_TITLE1 = "CYBERARK WHITE PHOENIX\n"
    EULA_TITLE2 = "SOFTWARE LICENSE AGREEMENT\nFor Non-Production Use Only"

    eula_text.insert(tk.END, EULA_TITLE1, "Title1")
    eula_text.insert(tk.END, EULA_TITLE2, "Title2")


def create_text1(eula_text):
    """
    create the text before the table
    """

    EULA_TEXT_BOLD = dict()
    EULA_TEXT = dict()

    EULA_TEXT0 = "\n\n\nCYBERARK SOFTWARE LTD. AND/OR ITS AFFILIATES (“CYBERARK”) IS WILLING TO LICENSE CYBERARK’S WHITE PHOENIX SOFTWARE (“SOFTWARE”) TO YOU AS THE COMPANY OR THE LEGAL ENTITY THAT WILL BE UTILIZING THE SOFTWARE (REFERENCED BELOW AS “YOU” OR “YOUR”) ON THE CONDITION THAT YOU ACCEPT ALL OF THE TERMS OF THIS SOFTWARE AGREEMENT (“AGREEMENT”).  IF YOU ENTER INTO THIS AGREEMENT ON BEHALF OF AN ENTITY OR ORGANIZATION, YOU REPRESENT THAT YOU HAVE THE LEGAL AUTHORITY TO BIND THAT ENTITY OR ORGANIZATION TO THIS AGREEMENT. YOU AND CYBERARK MAY EACH ALSO BE REFERRED TO AS A “PARTY” AND TOGETHER, THE “PARTIES”.PLEASE READ THIS AGREEMENT CAREFULLY BEFORE USING THE SOFTWARE. THIS IS A LEGAL AND ENFORCEABLE CONTRACT BETWEEN YOU AND CYBERARK.  BY INDICATING CONSENT ELECTRONICALLY, OR INSTALLING OR OTHERWISE USING THE SOFTWARE, YOU AGREE TO THE TERMS AND CONDITIONS OF THIS AGREEMENT.  IF YOU DO NOT AGREE TO THIS AGREEMENT, DO NOT INDICATE CONSENT ELECTRONICALLY AND MAKE NO FURTHER USE OF THE SOFTWARE. \n\n\n"

    EULA_TEXT_BOLD[1] = "1. License Rights; Non-Production use only."
    EULA_TEXT[
        1] = """ Subject to Your compliance with the terms and conditions of this Agreement, CyberArk grants to You a non-exclusive, non-transferable license to use a reasonable number of copies of the Software solely for your internal business purposes. THE SOFTWARE MAY ONLY BE USED IN NON-PRODUCTION ENVIRONMENTS. ALL DATA ENTERED INTO THE SOFTWARE BY OR FOR YOU, OR IS ASSOCIATED WITH THE USE OF THE SOFTWARE IN ANY MANNER, MAY BE PERMANENTLY LOST OR INACCESSIBLE, INCLUDING ALL DATA THAT IS STORED IN A DATABASE THAT YOU ELECT TO USE IN CONNECTION WITH THE SOFTWARE. \n\n"""
    EULA_TEXT_BOLD[2] = "2. License Restrictions."
    EULA_TEXT[
        2] = """ You may not, without CyberArk’s prior written consent, conduct, cause or permit the: (i) use, copying, modification, rental, lease, sublease, sublicense, or transfer of the Software except as expressly provided in this Agreement; (ii) creation of any derivative works based on the Software, except as expressly provided in this Agreement; (iii) reverse engineering, disassembly, or decompiling of the Software; (iv) use of the Software by any party other than You, except as expressly provided in this Agreement; (v) use the Software in any production environment; or (vi) use the Software in violation of any applicable law, statute, ordinance or regulation (including but not limited to the laws and regulations governing unauthorized access to computer networks, computer fraud and abuse, data protection and privacy).\n\n"""
    EULA_TEXT_BOLD[3] = "3. Ownership/Title."
    EULA_TEXT[
        3] = """ CyberArk and its licensors retain any and all rights, title and interest in and to the Software. Your rights to use the Software shall be limited to those expressly granted in this Agreement. All rights not expressly granted to You are retained by CyberArk and/or its licensors.\n\n"""
    EULA_TEXT_BOLD[4] = "4. Third Party Programs."
    EULA_TEXT[
        4] = """ This Software may contain third party software programs that are available under open source or free software licenses (“Third Party Programs”). Third Party Programs, even if included with the Software, are governed by separate license terms, including without limitation, open source software license terms. Such separate license terms (and not this Agreement) solely govern Your use of such Third Party Programs.\n\n"""
    EULA_TEXT_BOLD[5] = "5. Warranty Disclaimer and Limitation of Liability."
    EULA_TEXT[
        5] = """\n5.1. WARRANTY DISCLAIMER. THE SOFTWARE IS PROVIDED “AS IS,” EXCLUSIVE OF ANY WARRANTY OR REPRESENTATION, INCLUDING, WITHOUT LIMITATION, ANY IMPLIED WARRANTY OF MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, NONINFRINGEMENT, OR ANY OTHER WARRANTY, WHETHER EXPRESSED OR IMPLIED. YOU ASSUME ALL RISKS AND ALL COSTS ASSOCIATED WITH YOUR USE OF THE SOFTWARE. YOUR SOLE AND EXCLUSIVE REMEDY IN CASE OF ANY DISSATISFACTION OR DAMAGES IS TERMINATION OF THIS AGREEMENT. YOU AKNOWLEDGE THAT THE SOFTWARE IS LIKELY TO CONTAIN BUGS AND MAY NOT ALWAYS PERFORM AS SPECIFIED AND IS NOT SUITABLE FOR USE IN A PRODUCTION ENVIRONMENT. THUS, YOU ARE SOLELY RESPONSIBLE FOR ASCERTAINING THE FITNESS OF THE SOFTWARE FOR YOUR INTENDED USE, AND FOR CHECKING THAT THE SOFTWARE IS SUFFICIENTLY FREE FROM ERROR AND MALFUNCTION FOR SUCH USE. CYBERARK IS NOT RESPONSIBLE OR LIABLE FOR THE DELETION OF OR FAILURE TO STORE ANY OF YOUR DATA AND OTHER INFORMATION MAINTAINED IN CONNECTION WITH THE SOFTWARE. ALL DATA ENTERED INTO THE SOFTWARE BY OR FOR YOU, OR IS ASSOCIATED WITH THE USE OF THE SOFTWARE IN ANY MANNER, MAY BE PERMANENTLY LOST OR INACCESSIBLE, INCLUDING ALL DATA THAT IS STORED IN A DATABASE THAT YOU ELECT TO USE IN CONNECTION WITH THE SOFTWARE. YOU ARE THEREFORE ADVISED TO USE THE SOFTWARE ONLY WITH A DATABASE WHICH DOES NOT CONTAIN DATA THAT YOU WISH NOT TO BE LOST OR INACCESSIBLE. YOU ARE SOLELY RESPONSIBLE FOR SECURING AND BACKING UP SUCH DATA AND INFORMATION.\n\n5.2. LIMITATION OF LIABILITY.  TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW AND REGARDLESS OF WHETHER ANY REMEDY SET FORTH HEREIN FAILS OF ITS ESSENTIAL PURPOSE, IN NO EVENT WILL CYBERARK BE LIABLE TO YOU FOR ANY DIRECT, SPECIAL, CONSEQUENTIAL, INDIRECT OR SIMILAR DAMAGES, INCLUDING ANY LOST PROFITS OR LOST DATA, ARISING OUT OF THE USE OR INABILITY TO USE THE SOFTWARE, EVEN IF CYBERARK HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. SOME STATES AND COUNTRIES, INCLUDING MEMBER COUNTRIES OF THE EUROPEAN ECONOMIC AREA, DO NOT ALLOW THE LIMITATION OR EXCLUSION OF LIABILITY FOR INCIDENTAL OR CONSEQUENTIAL DAMAGES SO THE ABOVE LIMITATION OR EXCLUSION MAY NOT APPLY TO YOU.\n\n"""
    EULA_TEXT_BOLD[6] = "6. No Support or Maintenance."
    EULA_TEXT[6] = """ CyberArk does not offer any support or maintenance services for the Software. \n\n"""
    EULA_TEXT_BOLD[7] = "7. Confidentiality."
    EULA_TEXT[
        7] = """ You understand and acknowledge that the Software consists of valuable proprietary and confidential information of CyberArk, the use of which is subject to terms and conditions of this Agreement. You will take all reasonable steps necessary to ensure that the Software or any confidential information relating to it is not made available or disclosed to any third party. \n\n"""
    EULA_TEXT_BOLD[8] = "8. Export Control Regulation."
    EULA_TEXT[
        8] = """ You acknowledge that the Software and related technical data and services may be subject to the import and export control laws of the United States (specifically the U.S. Export Administration Regulations (EAR)), the State of Israel, and the laws of any country where the Software is imported or re-exported.  You agree to comply with all relevant laws and not to export or re-export the Software in contravention to U.S. law and other applicable laws nor to any prohibited country, entity, or person for which an export license or other governmental approval is required.\n\n"""
    EULA_TEXT_BOLD[9] = "9. Term and Termination."
    EULA_TEXT[
        9] = """ This Agreement will continue as long as You are in compliance with its terms, unless it was terminated by CyberArk with prior notice.  In the event You breach this Agreement, it will automatically terminate.  Upon termination, You must immediately stop using and destroy all copies of the Software within Your possession or control.  The Ownership/Title, Warranty and Limitation of Liability, Term and Termination, and General sections of this Agreement will survive termination of the Agreement.\n\n"""
    EULA_TEXT_BOLD[10] = "10. CyberArk Contracting Party, Choice of Law and Exclusive Jurisdiction."
    EULA_TEXT[10] = """ Each party agrees to the applicable governing law below without regard to choice or conflicts of law rules, and to the exclusive jurisdiction of the applicable courts below with respect to any dispute, claim, action, suit or proceeding (including non-contractual disputes or claims) arising out of or in connection with this Agreement, or its subject matter or formation.\n\n"""

    eula_text.insert(tk.END, EULA_TEXT0, "normal")
    for i in range(1, 11):
        eula_text.insert(tk.END, EULA_TEXT_BOLD[i], "bold")
        weight = "normal" if i != 5 else "bold"
        eula_text.insert(tk.END, EULA_TEXT[i], weight)


def create_table(eula_frame):
    """
    create the table part
    """

    table = [
        ["CyberArk entity entering into Agreement:", " With Principal Office at:", "Choice of Law:",
         "Exclusive Jurisdiction:"],
        ["CyberArk Software, Inc.", "60 Wells Avenue,\nNewton, MA 02459, U.S.A.",
         "Laws of Commonwealth of Massachusetts, U.S.A.", "Courts of Boston, Massachusetts, U.S.A."],
        ["Cyber-Ark Software (UK) Ltd.", "One Pear Place, 152-158 Waterloo Road, London, SE1 8BT, U.K.",
         "Laws of England and Wales", "Courts of London, England"],
        ["CyberArk Software Ltd.", "9 Hapsagot St. Park Ofer 2, P.O. Box 3143, Petach-Tikva 4951040, Israel",
         "Laws of Israel", "Courts of Tel Aviv Jaffa, Israel"],
        ["CyberArk Software Canada Inc.",
         "TD Canada Trust Tower, 161 Bay Street, 27th Floor, PO Box 508 Toronto, Ontario, M5J 2S1, Canada",
         "Laws of Ontario and the federal laws of Canada applicable therein", "Courts of Toronto, Ontario, Canada"],
        ["CyberArk Software (Singapore) Pte. Ltd.",
         "250 North Bridge Road, #14-01, Raffles City Tower, Singapore 179101", "Laws of Singapore",
         "Courts of Singapore"],
        ["CyberArk Software (Japan) K.K.", "Pacific Century Place 13F, 1-11-1, Marunouchi, Chiyoda-ku, Tokyo, Japan",
         "Laws of Japan", "Courts of Tokyo, Japan"],
        ["CyberArk Software (India) Private Limited",
         "My Home Twitza, 4th Floor, Plot Nos.30/A, Survey No.83/1, Beside Skyview, APIIC - Hyderabad Knowledge City, Hyderabad Telangana 500081",
         "Laws of India", "Courts of Hyderabad, India"],
        ["CyberArk Software (Australia) Pty Ltd", "Suite 6.0.1, Level 6, 55 Clarence St. Sydney NSW 2000",
         "Laws of Victoria, Australia", "Courts of Melbourne, Australia"]
    ]

    frame = tk.Frame(eula_frame)

    width = 27

    for i in range(len(table)):
        for j in range(len(table[i])):
            if i == 0:
                e = tk.Text(frame, width=width, height=5, wrap="word", bg="light gray", font=('Calibri', 10, 'bold'))
            else:
                e = tk.Text(frame, width=width, height=5, wrap="word", font=('Calibri', 10))
            e.grid(row=i, column=j)
            e.insert(tk.END, table[i][j])

    return frame


def create_text2(eula_text):
    """
    create the text after the table
    """
    EULA_TEXT10_2 = """To the extent not prohibited by law, each of the parties hereby irrevocably waives any and all right to trial by jury in any legal proceeding arising out of or related to this Agreement.\n\n"""
    EULA_TEXT_BOLD11 = "11. General."
    EULA_TEXT11 = """ You may not assign the rights granted hereunder or this Agreement, in whole or in part and whether by operation of contract, law or otherwise, without CyberArk’s prior express written approval. CyberArk may audit Your use of the Software. If any provision of this Agreement is found partly or wholly illegal or unenforceable, such provision shall be enforced to the maximum extent permissible, and remaining provisions of this Agreement shall remain in full force and effect.  A waiver of any breach or default under this Agreement shall not constitute a waiver of any other subsequent breach or default.  This Agreement is the complete and exclusive agreement between You and CyberArk relating to the Software and supersedes any previous or contemporaneous oral or written communications, proposals, and representations with respect to its subject matter.\n\n"""
    eula_text.insert(tk.END, EULA_TEXT10_2, "normal")
    eula_text.insert(tk.END, EULA_TEXT_BOLD11, "bold")
    eula_text.insert(tk.END, EULA_TEXT11, "normal")


def create_text_styles(eula_text):
    """
    define the various styles for the text
    """
    eula_text.tag_configure("Title1", font=("Calibri", 12, "bold"), justify="center")
    eula_text.tag_configure("Title2", font=("Calibri", 12, "bold", "underline"), justify="center")
    eula_text.tag_configure("bold", font=("Calibri", 10, "bold"))
    eula_text.tag_configure("Normal", font=("Calibri", 10, "normal"))


def create_buttons(eula_window):
    """
    create the "accept" and "decline" buttons for the EULA
    """

    # Create a button to accept the EULA and close the popup window
    def accept_eula():
        """
        if accepted set EULAAccepted value in White Phoenix registry key to 1
        """
        EULA_ACCEPTED_REG_KEY = r"SOFTWARE\White Phoenix"
        EULA_ACCEPTED_REG_VALUE = "EULAAccepted"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, EULA_ACCEPTED_REG_KEY)
        winreg.SetValueEx(key, EULA_ACCEPTED_REG_VALUE, 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        eula_window.destroy()

    # Create Decline Button
    accept_button = tk.Button(eula_window, text="Decline", command=eula_window.destroy)
    accept_button.pack(side=tk.RIGHT, padx=5, pady=5)
    # Create Accept Button
    accept_button = tk.Button(eula_window, text="Accept", command=accept_eula)
    accept_button.pack(side=tk.RIGHT, pady=5)


def create_texts(frame2):
    """
    create both text widgets for before and after the table
    return: both text widgets
    """
    width = 96

    eula_text = tk.Text(frame2, wrap="word", width=width, height=100)
    create_title(eula_text)
    create_text1(eula_text)

    eula_text2 = tk.Text(frame2, wrap="word", width=width, height=15)
    create_text2(eula_text2)
    eula_text2.grid(row=2, column=0)

    create_text_styles(eula_text)
    create_text_styles(eula_text2)

    return eula_text, eula_text2


def create_eula():
    """
    Create a EULA window and update a registry key when accepted
    """
    eula_window = create_main_window()

    frame, frame2 = create_frames_and_canvas(eula_window)

    eula_text, eula_text2 = create_texts(frame2)
    table_frame = create_table(frame2)

    eula_text.grid(row=0, column=0)
    table_frame.grid(row=1, column=0)
    eula_text2.grid(row=2, column=0)

    create_buttons(eula_window)
    eula_window.mainloop()
