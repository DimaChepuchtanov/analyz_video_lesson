from API.database.user import DataBaseUser
from API.server.user import MiddleLoyerUser
from API.database.company import DataBaseCompany
from API.server.company import MiddleLoyeCompany
from API.database.licenses import DataBaseLicences
from API.server.licenses import MiddleLoyerLicences
from API.database.role import DataBaseRole
from API.server.role import MiddleLoyerRole
from API.database.lessons import DataBaseLessons
from API.server.lessons import MiddleLoyeLesson
from API.database.file import DataBaseFile
from API.server.file import MiddleLoyerFile
from API.database.token import DataBaseToken
from API.server.token import MiddleLoyerToken


user_logic = MiddleLoyerUser(DataBaseUser())
company_logic = MiddleLoyeCompany(DataBaseCompany())
license_logic = MiddleLoyerLicences(DataBaseLicences())
role_logic = MiddleLoyerRole(DataBaseRole())
lesson_logic = MiddleLoyeLesson(DataBaseLessons())
file_logic = MiddleLoyerFile(DataBaseFile())
token_logic = MiddleLoyerToken(DataBaseToken())
