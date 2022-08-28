# Team Input Now
@client.command()
async def team(ctx, sheet_name, tab_site, api_token):
    global gsclient
    await ctx.send("Connecting to your sheet...")
    sheet = gsclient.open(sheet_name).sheet1
    await ctx.send('Connected Successfully!')

    # connecting with tab site
    await ctx.send("Connecting to your tab site...")
    if tab_site.endswith('/'):
        x = tab_site.split('/')
        slug = x[-2]
        mainSite = x[0] + "//" + x[2]

        print(mainSite, slug)
        await ctx.send("Connected!")
        await ctx.send(f"Your sheet **{sheet_name}** has successfully connected with {mainSite}")
    else:
        x = tab_site.split('/')
        slug = x[-1]
        mainSite = x[0] + "//" + x[2]

        print(mainSite, slug)
        await ctx.send("Connected!")
        await ctx.send(f"Your sheet **{sheet_name}** has successfully connected with {mainSite}")

    await ctx.send(f"Starting Adj Input...")
    

    r = requests.get(
        f'{mainSite}/api/v1/institutions',
        headers={
                'Authorization': 'token '+api_token
                })
                 
    institutions = r.json()
    
    
    code = sheet.col_values(3)
    col_name = sheet.col_values(2)
    x = 1
    k = 2

    while x < len(col_name):
        team_row = sheet.row_values(k)
        institution = None
        name = team_row[1]

        ins_code = code[x]
        
        
        x += 1
        
        await ctx.send(f"Getting the institution data for {name} ...")
        for i in institutions:
            if i['code'] == ins_code:
                institution = i['url']
                await ctx.send(f"Institution - {ins_code}")
                break

            elif adj_row[3] == 'x':
                await ctx.send(f"No Institution!")
                break
        
        await ctx.send(f"Input for **{name}** is starting...")
        
        # Gender
        # 1
        if team_row[5] == "Male":
            gender_1 = 'M'
            # print(gender)
        elif team_row[5] == "Female":
            gender_1 = 'F'
        else:
            gender_1 = 'O'

        # 2
        if team_row[8] == "Male":
            gender_2 = 'M'
            # print(gender)
        elif team_row[8] == "Female":
            gender_2 = 'F'
        else:
            gender_2 = 'O' 

        # 3
        if team_row[11] == "Male":
            gender_3 = 'M'
            # print(gender)
        elif team_row[11] == "Female":
            gender_3 = 'F'
        else:
            gender_3 = 'O'     
            
        
        # Mail
        name_new = team_row[1]

        member_1 = team_row[3]
        email_1 = team_row[4]
        
        member_2 = team_row[6]
        email_2 = team_row[7]

        member_3 = team_row[9]
        email_3 = team_row[10]
        
    
        printa = f"{mainSite}/api/v1/tournaments/{slug}/teams"
        print(printa)
        r = requests.post(
            f'{mainSite}/api/v1/tournaments/{slug}/teams',
                json = {"reference": name_new,
                "short_reference": name_new,
                
                "institution":  "https://tabbyhero.herokuapp.com/api/v1/institutions/76",
                "speakers": [
                    {
                    "name": member_1,
                    "gender": gender_1,
                    "email": email_1,
                    "phone": "",
                    "anonymous": False,
                    "pronoun": "",
                    "categories": [],
                    "url_key": ""
                    },
                    {
                    "name": member_2,
                    "gender": gender_2,
                    "email": email_2,
                    "phone": "",
                    "anonymous": False,
                    "pronoun": "",
                    "categories": [],
                    "url_key": ""
                    },
                    {
                    "name": member_3,
                    "gender": gender_3,
                    "email": email_3,
                    "phone": "",
                    "anonymous": False,
                    "pronoun": "",
                    "categories": [],
                    "url_key": ""
                    }
                ],
                "use_institution_prefix": False,
                "break_categories": [],
                "institution_conflicts": []
                },

                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'token '+api_token
                    })
        
        status = r.status_code
        print(f"{status}: {name}, {institution}")
        await ctx.send(f"Input for **{name}** has been successfully done!\n**.**")
        
        if status != 201:
            await ctx.send(f"Error occured while posting {name}, {institution}\n Error {status}\n{r.text}")

        if x == len(col_name):
            await ctx.send("**All input has been finished!**")

        
        k += 1
