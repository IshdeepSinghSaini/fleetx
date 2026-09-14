@echo off
set JAVA_HOME=C:\Oracle_JDK-24
set PATH=C:\Oracle_JDK-24\bin;%PATH%
call .\mvnw.cmd spring-boot:run
