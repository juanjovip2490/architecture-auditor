"use strict";var R=Object.create;var g=Object.defineProperty;var O=Object.getOwnPropertyDescriptor;var W=Object.getOwnPropertyNames;var A=Object.getPrototypeOf,z=Object.prototype.hasOwnProperty;var B=(e,t)=>{for(var n in t)g(e,n,{get:t[n],enumerable:!0})},M=(e,t,n,o)=>{if(t&&typeof t=="object"||typeof t=="function")for(let r of W(t))!z.call(e,r)&&r!==n&&g(e,r,{get:()=>t[r],enumerable:!(o=O(t,r))||o.enumerable});return e};var C=(e,t,n)=>(n=e!=null?R(A(e)):{},M(t||!e||!e.__esModule?g(n,"default",{value:e,enumerable:!0}):n,e)),I=e=>M(g({},"__esModule",{value:!0}),e);var H={};B(H,{activate:()=>D,deactivate:()=>L});module.exports=I(H);var s=C(require("vscode"));function h(){let e="",t="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(let n=0;n<32;n++)e+=t.charAt(Math.floor(Math.random()*t.length));return e}function b(e){let t=h();return`<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Security-Policy" content="
            default-src 'none';
            script-src 'nonce-${t}' https://cdn.jsdelivr.net;
            style-src ${e.cspSource} 'unsafe-inline';
            font-src ${e.cspSource};
        ">
        
        <script src="https://cdn.jsdelivr.net/npm/markdown-it@14.1.0/dist/markdown-it.min.js" integrity="sha256-OMcKHnypGrQOLZ5uYBKYUacX7Rx9Ssu91Bv5UDeRz2g=" crossorigin="anonymous"></script>        
        <style>
            * {
                font-size: 18px;
            }
            body { 
                margin: 0;
                padding: 20px;
                height: calc(100dvh - 40px); /* Fixed calculation syntax */
                width: calc(100dvw - 40px);  /* Fixed calculation syntax */
                display: flex;
                flex-direction: column;
                gap: 20px;
                background-color: var(--vscode-editor-background);
                color: var(--vscode-editor-foreground);
                box-sizing: border-box;      /* Added for proper sizing */
            }
    
            #response-container {
                flex: 1;
                overflow-y: auto;
                background-color: var(--vscode-editorWidget-background);
                border: 1px solid var(--vscode-editorWidget-border);
                border-radius: 4px;
                padding: 15px;
                min-height: 450px;
            }
    
            .input-container {
                gap: 10px;
                height: fit-content;
            }
    
            #user-input { 
                flex: 1;
                padding: 15px;
                width: 100%;
                border: 1px solid var(--vscode-input-border);
                background-color: var(--vscode-input-background);
                color: var(--vscode-input-foreground);
                font-family: var(--vscode-editor-font-family);
                border-radius: 3px;
                resize: vertical;  /* Allows vertical resizing only */
                min-height: 100px; /* Minimum height */
                max-height: 70vh;  /* Maximum height (70% of viewport height) */
                overflow-y: auto;  /* Show scrollbar when content exceeds height */                box-sizing: border-box;
            }
    
            #send-button {
                width: 100px; 
                padding: 10px 20px;
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                border-radius: 3px;
                cursor: pointer;
                transition: opacity 0.2s;
                align-self: flex-end;
                height: fit-content;
            }
    
            #send-button:hover {
                opacity: 0.8;
            }
    
            #send-button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
    
            .response-text {
                line-height: 1.5;
                font-family: var(--vscode-editor-font-family);
            }
    
            .typing-cursor {
                display: inline-block;
                width: 8px;
                background: var(--vscode-editor-foreground);
                animation: blink 1s step-end infinite;
            }
    
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }

            #sources {
                overflow: auto; 
                max-height: 20dvh; 
                margin-top: 15px;
                border-top: 1px solid var(--vscode-editorWidget-border);
                padding-top: 10px;
                font-size: 0.9em;
            }

            #sources div {
                margin: 5px 0;
                padding-left: 15px;
                position: relative;
            }

            #sources div::before {
                position: absolute;
                left: 0;
                color: var(--vscode-editor-foreground);
            }
            .userMessage { 
                color: #00fff7; 
                font-size: 2rem; 
                text-align: right;
            }

        </style>
    </head>
    <body>
        <div id="sources">
        </div> 
        <div id="response-container">

            <div id="response-text" class="response-text">
            </div>
            <div id="current-message"> </div> 
        </div>
    
        <div class="input-container">
            <textarea  
                id="user-input" 
                placeholder="Enter your code question... Hit Enter to send. Hit Shift + Enter to add another line"
                spellcheck="false"
            ></textarea>

        </div>
    
        <script nonce="${t}">

            // Markdown parser to render the response text 
            const md = window.markdownit({
                breaks: true, 
                linkify: true, 
                typographer: true,
                html: true
            });

            const vscode = acquireVsCodeApi();
            const input = document.getElementById('user-input');
            let userPrompt = "", userPromptPrefixDiv = '\\n\\n<div class="userMessage" >', userPromptSuffixDiv = ' </div>\\n\\n';
            const responseText = document.getElementById('response-text');
            const currentResponseText = document.getElementById("current-message");
            let cursorElement = null;
            let responseTextMessageForContext = ""; 
        // Handle Enter key (Shift+Enter for newline)
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                currentResponseText.innerText += userPromptPrefixDiv + input.value + userPromptSuffixDiv;
                userPrompt = input.value; 
                sendMessage();
            }
        });


            // This function is called when the message is complete and we want to send the context back to the parent window for future messages
            function sendContext(prompt, response) { 
                vscode.postMessage({
                    command: "setContext",
                    prompt: prompt,
                    response: response 
                })
            }


            function removeThinkings(text) {

                    //The reasoning tokens are removed from the response text. Everything between <think> and </think> is a reasoning token returned by the model and we don't want the chat to be cluttered with them.
                    const indexOfStartReasoningTokens = currentResponseText.innerText.indexOf("<think>");
                    const indexOfEndReasoningTokens = currentResponseText.innerText.indexOf("</think>");    
                    return text.slice(0, indexOfStartReasoningTokens) + text.slice(indexOfEndReasoningTokens + 8, text.length).trim();
                }

            window.addEventListener('message', event => {
                const message = event.data;
                let streamChunk = ""; 
                const sourcesList = document.getElementById("sources");

                if (message.command === "stream") {
                    // Append streaming text safely
                    currentResponseText.innerText += message.content;

                    //Scroll to the bottom of the response container
                    const responseContainer = document.getElementById('response-container');
                    responseContainer.scrollTop = responseText.scrollHeight;

                } else if (message.command === "complete") {
            
                    // Remove the "thinking" tokens from the response text
                    currentResponseText.innerText = removeThinkings(currentResponseText.innerText); 

                    // Extract the user prompt from the response text 
                    responseTextMessageForContext = currentResponseText.innerText.split(userPromptSuffixDiv)[1]; 
                    
                    // Render the final response text and remove the "current response" text
                    currentResponseText.innerHTML =   md.render(currentResponseText.innerText)
                    responseText.insertAdjacentHTML('beforeend', currentResponseText.innerHTML);
                    currentResponseText.innerText = "";
                    currentResponseText.style.whiteSpace = 'pre-wrap';

                    // Send back the context (being just the users' prompt essentially) to the parent window. No need to send the response as it is already stored in the parent window
                    sendContext(userPrompt, responseTextMessageForContext); 

                    // Allow the user to type again 
                    input.readOnly = false;

                } else if (message.command === "source") {
                    // Create new source element with Markdown parsing
                    const sourceItem = document.createElement('div');
                    sourceItem.innerHTML = md.render('- ' + message.content);
                    sourcesList.prepend(sourceItem);  // Add to top of sources list
                }
            });


            // Send message to extension

            function sendMessage() {
                const message = input.value.trim();
                if (message) {
                    
                    input.readOnly = true;
                    vscode.postMessage({
                        command: 'submit',
                        content: message
                    });
                    input.value = '';
                }
            }


        </script>
    </body>
    </html>
    `}async function k({message:e,context:t,model:n,apiKey:o,sendContentToInnerWebView:r}){let i={model:n,messages:[{role:"system",content:"Make sure you are correct!"},...t,{role:"user",content:e}],stream:!0};try{let c=await fetch("https://api.perplexity.ai/chat/completions",{method:"POST",headers:{Authorization:`Bearer ${o}`,"Content-Type":"application/json",Accept:"application/json"},body:JSON.stringify(i)});if(!c.ok){let f=await c.json();r({command:"error",content:f})}let a=c.body?.getReader(),v=new TextDecoder,u=[],d="";for(;;){let{done:f,value:S}=await a.read();if(f){await u.forEach(m=>{r({command:"source",content:m})}),console.log("Processed response from Perplexity"),r({command:"complete"});return}for(d+=v.decode(S,{stream:!0});d.includes(`
`);){let m=d.indexOf(`
`),P=d.slice(0,m).trim();if(d=d.slice(m+1),P.startsWith("data: "))try{let w=P.replace("data: ",""),l=JSON.parse(w);if(l.choices[0]?.finished_reason==="stop"){r({command:"complete"});return}else if(l.choices[0]?.finished_reason)throw Error(l.choices[0]?.finished_reason);let y=l.choices[0]?.delta?.content||"";if(u=l.citations,y&&(r({command:"stream",content:y}),y.finished_reason)){r({command:"complete"});return}}catch(w){r({command:"error",content:w})}}}}catch(c){throw new Error(`Failed to complete request: ${c?.message||"Unknown error"}`)}}var x=C(require("vscode"));var E=["sonar","sonar-pro","sonar-reasoning","sonar-reasoning-pro","sonar-deep-research"];function T(e){let t=h();return`<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Security-Policy" content="
            default-src 'none';
            style-src ${e.cspSource} 'unsafe-inline';
            font-src ${e.cspSource};
            script-src 'nonce-${t}' ${e.cspSource};
        ">
        
        <style>
            * {
                font-size: 18px;
                font-family: var(--vscode-editor-font-family);
            }
            body { 
                margin: 0;
                padding: 20px;
                height: 100%;
                width: 100%; 
                display: flex;
                flex-direction: column;
                gap: 20px;
                background-color: var(--vscode-editor-background);
                color: var(--vscode-editor-foreground);
                box-sizing: border-box;      /* Added for proper sizing */
            }
    
            .input-container {
                gap: 10px;
                height: fit-content;
            }
        
            #send-button {
                width: 100%;
                padding: 10px 20px;
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                cursor: pointer;
                transition: opacity 0.2s;
                align-self: flex-end;
                height: fit-content;
            }
    
            #send-button:hover {
                opacity: 0.8;
            }

            select {
                padding: 10px 20px;
                border: none;
                width: 100%;
                background-color: var(--vscode-input-background);
                color: var(--vscode-editor-foreground); 
            }

            select:focus {
                outline: none;
            }
        </style>
    </head>
    <body>

            <h1>Perplexity Chat</h1>

            <h3> Click the button below to open the chat window </h3>
            <button id="send-button">Open Chat Window</button>

            <h3>  Select your preferred model </h3>
            <select name="Model" id="model-selector" required>
                ${E.map(o=>(console.log("Loaded model "+o),"<option value="+o+">"+o+"</option>")).join("")}
            </select>
    

            <script nonce="${t}"> 
                
                const vscode = acquireVsCodeApi();
                const button  = document.getElementById('send-button');
                
                button.addEventListener('click', () => {
                    vscode.postMessage({
                        command: 'openChatWindow'
                    });
                });


                // Send message to the parent window once the user selects a model
                const dropdown = document.getElementById('model-selector');
                dropdown.addEventListener('change', (e) => {
                    vscode.postMessage({
                            command: 'selectModel',
                            content: e.target.value
                    });
                });

            </script>
    </body>
    </html>
    `}var p=class e{_view;getWebviewContent(){return T(this._view.webview)}static viewType="perplexityChatView";static model="sonar";resolveWebviewView(t,n,o){this._view=t,t.webview.options={enableScripts:!0},t.webview.html=this.getWebviewContent(),t.webview.onDidReceiveMessage(r=>{try{switch(r.command){case"openChatWindow":console.log("Opening Chat Window"),x.commands.executeCommand("perplexity-ext.openChatWindow");return;case"selectModel":console.log("Selecting model: "+r.content),e.model=r.content;break}}catch(i){x.window.showErrorMessage(i.what())}})}};function D(e){s.commands.registerCommand("perplexity-ext.setAPIToken",()=>{s.window.showInputBox({prompt:"Enter your API key",placeHolder:"e.g. pplx-...1234",title:"Set API Key for Perplexity"}).then(async o=>{o?await e.secrets.store("perplexity-ext.apiKey",o):s.window.showErrorMessage("No API Token Provided!")})});let t=s.commands.registerCommand("perplexity-ext.openChatWindow",async()=>{let o=[],r="sonar",i=s.window.createWebviewPanel("perplexity","Perplexity Chat",s.ViewColumn.One,{enableScripts:!0,localResourceRoots:[e.extensionUri],retainContextWhenHidden:!0}),c=await e.secrets.get("perplexity-ext.apiKey");i.webview.onDidReceiveMessage(async a=>{if(!c)s.window.showErrorMessage("API key not configured");else switch(a.command){case"submit":try{await k({message:a.content,context:o,model:p.model,apiKey:c,sendContentToInnerWebView:i.webview.postMessage.bind(i.webview)})}catch(d){i.webview.postMessage({command:"error",error:d.message})}break;case"webviewError":console.error(a.content);break;case"setContext":console.log("Setting context: "+a.response);let v={role:"user",content:a.prompt??"NO PROMPT"},u={role:"assistant",content:a.response??"NO RESPONSE"};o.push(v),o.push(u),o.length>16&&(o.shift(),o.shift()),console.log(o)}},void 0,e.subscriptions),i.webview.html=b(i.webview)}),n=new p;e.subscriptions.push(s.window.registerWebviewViewProvider(p.viewType,n)),e.subscriptions.push(t)}function L(){}0&&(module.exports={activate,deactivate});
