var fs = require('fs'); 
const args = process.argv.slice(2);
var path = require('path');
var root = path.dirname(require.main.filename);
var extension=null;
var substr=null;
var count=0;

main();

function main()
{
	if(test_args())
	{
		phrase(args[0],args[1]);
		scan_all(root);
		if(count==0)
		{
			console.log("No file was found.");
		}
		else
		{
			console.log("found ",count," file(s).");
		}
	}
}
function test_args()
{
	
	if(args[0]==null || args[1]==null)
	{
		console.log("USAGE: node search [ext] [text]");
		return false;
	}
	if(args[2]!=null)
	{
		console.log("ERROR: too many arguments");
		return false;
	}
	return true;
}
function phrase(ext,str)
{
	console.log("Yair Zafrany Search Solution:");
	console.log("=============================");
	console.log("> working directory: ",root);
	console.log("> file extension: ",ext);
	console.log("> search for: ",str);
	extension=ext;
	substr=str;
}
function scan_all(dir)
{
	//console.log("directory: ",dir);
	var list=fs.readdirSync(dir);
	for(var i=0;i<list.length;i++)
	{
		
		entity=path.join(dir,list[i]);
		if(fs.lstatSync(entity).isFile())
		{
			//console.log("file: ",entity);
			check(entity);
			
		}
		else
		{
			scan_all(entity);
		}
			
	}
}
function check(file_path)
{
	if(path.extname(file_path)==extension)
	{
		var content = fs.readFileSync(file_path);
		if(String(content).includes(substr))
		{
			console.log(file_path);
			count++;
		}
	}
}


