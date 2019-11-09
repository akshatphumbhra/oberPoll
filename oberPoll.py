from flask import *

#SQLAlchemy- -Database
#https://www.youtube.com/watch?v=QjtW-wnXlUY -- Tutorial

app = Flask(__name__)
#add a basedir that can be called 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'\
#possibly change this to SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \'sqlite:///' + os.path.join(basedir, 'app.db')
#and SQLALCHEMY_TRACK_MODIFICATIONS = False

db=SQLAlchemy(app) #creates database db


@app.route('/')
class index():
     id = db.Column(db.Integer, primary_key=True, unique=true, nullable=true) #does true and false need to be True and False
     name = db.Column(db.String(20), unique=true, nullable = false)
    # db.add({"name":"Akshat"})
    # db.commit()
    # print(db.query(1))
    return render_template("index.html")

@app.route('/Akshat')
def akshat():
    return "<h1> Henry sucks!</h1>"

if __name__ == "__main__":
    app.run(debug=True)

# -- ---
# -- Globals
# -- ---
# 
# -- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
# -- SET FOREIGN_KEY_CHECKS=0;
# 
# -- ---
# -- Table 'User'
# -- 
# -- ---
# 
# DROP TABLE IF EXISTS `User`;
# 		
# CREATE TABLE `User` (
#   `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
#   `Name` VARCHAR(64) NULL DEFAULT NULL,
#   `Paassword` VARCHAR(64) NULL DEFAULT NULL,
#   `Student?` BINARY(8) NULL DEFAULT NULL,
#   PRIMARY KEY (`id`)
# );
# 
# -- ---
# -- Foreign Keys 
# -- ---
# 
# 
# -- ---
# -- Table Properties
# -- ---
# 
# -- ALTER TABLE `User` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
# 
# -- ---
# -- Test Data
# -- ---
# 
# -- INSERT INTO `User` (`id`,`Name`,`Paassword`,`Student?`) VALUES
# -- ('','','','');