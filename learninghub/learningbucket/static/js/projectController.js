/*******************************************************
 * Controller for learningbucket/template/project.html
 *
 * @author Per-Henrik E Kvalnes 2014
 *****************************************************/
function initPage()
{
  loadTagLinker();
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
