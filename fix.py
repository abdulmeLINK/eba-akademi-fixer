import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

class fix():
	def makeReadyCfg(self,cfgFileName):
		cfg = configparser.ConfigParser()
		cfg.read(cfgFileName)
		return cfg
	def makeReadyBrowser(self,cfg):
		browser = webdriver.Chrome(cfg['paths']['chromedriver'])
		browser.get(cfg['EBAurls']['starturl'])
		return browser
	def loginWithCredentialsToEd(self,browser,cfg):
		browser.find_element_by_xpath(cfg['EBAxpaths']['loginWithEdevlet']).click()
		browser.find_element_by_id(cfg['EBAids']['tc']).send_keys(cfg['credentials']['TC'])
		browser.find_element_by_id(cfg['EBAids']['password']).send_keys(cfg['credentials']['Edevletpassword'])
		browser.find_element_by_name(cfg['EBAids']['Edevletsubmit']).click()
	def loginWithCredentialsToDefault(self,browser,cfg):
		browser.find_element_by_id(cfg['EBAids']['EBAtckn']).send_keys(cfg['credentials']['TC'])
		browser.find_element_by_id(cfg['EBAids']['EBApassword']).send_keys(cfg['credentials']['EBApassword'])
		browser.find_element_by_xpath(cfg['EBAxpaths']['EBAsubmit']).click()
	def menuFinder(self,browser,cfg,checker):
		while checker:
			try:
				headerChecker = WebDriverWait(browser, float(cfg['settings']['delay'])).until(EC.element_to_be_clickable((By.XPATH, cfg['EBAxpaths']['ebamenu'])))
				browser.find_element_by_xpath(cfg['EBAxpaths']['ebamenu']).click()
				checker=False
			except TimeoutException:
			    print(cfg['EBAxpaths']['ebamenu'] + ' aranırkan zaman aşımı... Tekrar deneniyor.')	
			except ElementClickInterceptedException:
				print(cfg['EBAxpaths']['ebamenu'] + 'öğesine tıklama engellendi.')
			except ElementNotInteractableException:
			 	print(cfg['EBAxpaths']['ebamenu'] + 'öğesi tıklanabilir değil.')				
	def ebadFinder(self,browser,cfg,checker):
		while checker:
			try:
			    myElem = WebDriverWait(browser, float(cfg['settings']['delay'])).until(EC.element_to_be_clickable((By.XPATH, cfg['EBAxpaths']['ebaadbtn'])))
			    cheker = False
			    browser.find_element_by_xpath(cfg['EBAxpaths']['ebaadbtn']).click()
			except TimeoutException:
				print(cfg['EBAxpaths']['ebaadbtn'] + ' aranırkan zaman aşımı... Tekrar deneniyor.')
	def insertBypassUrl(self,browser,cfg):
		browser.get(cfg['EBAurls']['admainbypassurl'])					
	def findContentHolder(self,browser,cfg,checker):
		while checker:
		   try:
			   LO = WebDriverWait(browser,float(cfg['settings']['delay'])).until(EC.presence_of_element_located((By.XPATH,cfg['EBAxpaths']['iframe'])))
			   browser.switch_to.frame(cfg['EBAframes']['contentholder'])
			   checker = False
		   except TimeoutException:
			   print('İçerik bulunamadı.')       
	def makeSourceReachable(self,browser,cfg,checker):
		while checker:
			try:
				WebDriverWait(browser,float(cfg['settings']['delay'])).until(EC.element_to_be_clickable((By.CLASS_NAME,cfg['EBAclassnames']['videoplayer'])))
				videocontainers = browser.find_elements_by_class_name(cfg['EBAclassnames']['videoplayer'])
				for v in videocontainers:
				  v.click()
				checker = False
			except NoSuchElementException:
				print(cfg['EBAclassnames']['videoplayer'] + ' öğesi bulunamadı')
			except TimeoutException:
				print(cfg['EBAclassnames']['videoplayer'] + ' aranırkan zaman aşımı... Tekrar deneniyor.')
			except ElementNotInteractableException:
				print(cfg['EBAclassnames']['videoplayer'] + ' öğesi erişilebilir değil el ile deneyin.')  
	def checkSourcesAndFix(self,browser,cfg):
		WebDriverWait(browser,float(cfg['settings']['delay'])).until(EC.presence_of_element_located((By.XPATH,cfg['EBAxpaths']['video'])))
		source = browser.find_elements_by_xpath(cfg['EBAxpaths']['video'])
		if source is not None:
			for m in source :
				lList = []
				for i in m.get_attribute("src"):
					if i == '?':
					  Link = ''.join(lList)
					  print(Link)
					else:
					  lList.append(i)
				
				if Link is not None:
					browser.execute_script('arguments[0].setAttribute("src","{}");'.format(Link), m)
					print(len(source)+' tane video düzeltildi.')
if __name__ == '__main__':
   fix = fix()
   cfg = fix.makeReadyCfg('config.ini')
   browser = fix.makeReadyBrowser(cfg)
   method = cfg['credentials']['method']
   if method == 'EBA':
      fix.loginWithCredentialsToDefault(browser,cfg)
   if method == 'EDEVLET':
      fix.loginWithCredentialsToEd(browser,cfg)
   fix.menuFinder(browser,cfg,True)
   fix.ebadFinder(browser,cfg,True)
   while browser.current_url == cfg['EBAurls']['main']:
	   fix.insertBypassUrl(browser,cfg)
   fix.findContentHolder(browser,cfg,True)
   fix.makeSourceReachable(browser,cfg,True)
   while cfg['settings'].getboolean('checkback'):
	   fix.checkSourcesAndFix(browser,cfg,True)


 	
