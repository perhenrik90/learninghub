/*******************************************************
 * Controller for learningbucket/template/project.html
 *
 * @author Per-Henrik E Kvalnes 2014
 *****************************************************/
function initPage()
{
    loadTagLinker();
    setupFileSelector();
}
window.addEventListener('load',initPage);

/******************************************************
 * Loops through comment class and links
 *  the tag to the searchbucket.view.searchProject 
 *****************************************************/
function loadTagLinker()
{
    comments = document.getElementsByClassName("comment");
    for (i in comments)
    {
	comment = comments[i];
	if(comment.children)
	{
	    str = comment.children[0].innerHTML;
	    str = appendLinksToString(str);
	    comment.children[0].innerHTML = str;
	}
    }

}


/*****************************************************************
 * Append anchors (a) to href <site>/search?tags=<tagsearchvalue 
 * not connected with views variable. If /search url is changed,
 * it must be updated in this script manualy.
 *****************************************************************/

function appendLinksToString(str)
{
    str = str.replace(/(#\S+)/g , "<a href='../search?tags=$1'>$1</a>");
    str = str.replace(/(=#)/g, "=%23");
    return str;
}


/*******************************
 * Sets up a selector box for 
 *  filtering files 
 *******************************/

function setupFileSelector()
{
    span = document.getElementById("fileselector");
    if(! span) { return 0;}

    select = document.createElement("select");
    span.appendChild(select);
    
    alloption = document.createElement("option");
    alloption.value = "";
    alloption.innerHTML = "-";
    select.appendChild(alloption);


    /** map files types to a dictionary **/
    dic =  {};
    filetypes = document.getElementsByClassName("fileTypeTd");
    for(i in filetypes)
    {
	type = filetypes[i]
	dic[type.innerHTML] = 1;
    }

    /** append options based on the dictionary **/
    for(key in dic)
    {
	if(key != 'undefined')
	{
	    option = document.createElement("option");
	    option.value = key;
	    option.innerHTML = key;
	    select.appendChild(option);
	}
    }

    /******************************
     * Selector event listener 
     ******************************/
    select.onchange = function(e)
    {
	tablerows = document.getElementsByClassName("fileTr");
	for(i = 0; i < tablerows.length; i++)
	{
	    row = tablerows[i];
	    row.style.display = "";
	    filetype = row.children[1].innerHTML
	    if(this.value != filetype && this.value != "")
	    {
		 row.style.display = "None";
	    }
	}
    }
}
