Name:		kotlin-compiler-embeddable
Version:	2.4.21
Release:	1
Summary:	Kotlin compiler embeddable for the JVM
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/JetBrains/kotlin
# Kotlin tag v2.4.21, commit 9180ce6a7a7d3627f88b424717583f28ddca052d.
# org.jetbrains.kotlin:kotlin-compiler-embeddable. The compiler modules are
# compiled with the installed kotlinc 2.0.21. Context-parameter syntax and a
# handful of 2.4 APIs are adapted in the staged tree. The staged tree already
# carries those edits, plus the rewrite marker, so the build does not run the
# rewriter again.
# Third-party classes (IntelliJ subset, ASM, protobuf runtime) are taken from
# the installed kotlin-compiler.jar and kept unrelocated. The 2.4 sources
# import those packages under their original names. vavr 0.10.4, kotlinx
# collections-immutable 0.5.1, the protobuf format, and the CRI serializer are
# compiled from the vendored sources in this tarball. javac-api is a JDK
# compile classpath only and is not shipped.
# stdlib, reflect, script-runtime, coroutines, atomicfu, and trove stay
# outside the jar.
# The jar name is versioned. kotlin-libs 2.0.21 keeps
# /usr/share/java/kotlin-compiler-embeddable.jar and its sysjar index.
Source0:	kotlin-compiler-embeddable-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-21-openjdk-devel
BuildRequires:	kotlin = 2.0.21
BuildRequires:	python
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-stdlib) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-reflect) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-script-runtime) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-build-tools-api) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlinx:kotlinx-coroutines-core-jvm) = 1.10.2
BuildRequires:	mvn(org.jetbrains.kotlinx:atomicfu-jvm) = 0.26.1
BuildRequires:	mvn(org.jetbrains.kotlinx:kotlinx-serialization-core) = 1.11.0
BuildRequires:	mvn(org.jetbrains:annotations) = 24.0.1
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(com.google.code.gson:gson)
BuildRequires:	mvn(com.google.code.findbugs:jsr305)
BuildRequires:	mvn(org.antlr:antlr4-runtime)
Requires:	kotlin = 2.0.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-stdlib) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-reflect) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-script-runtime) = 2.4.21
Requires:	mvn(org.jetbrains.kotlinx:kotlinx-coroutines-core-jvm) = 1.10.2
Requires:	mvn(org.jetbrains.kotlinx:atomicfu-jvm) = 0.26.1
Requires:	mvn(org.jetbrains.intellij.deps:trove4j)

%description
org.jetbrains.kotlin:kotlin-compiler-embeddable %{version}.
The Kotlin 2.4.21 compiler, compiled with kotlinc 2.0.21. The jar does not
replace the kotlin-libs 2.0.21 embeddable.

%prep
%autosetup -n kotlin-compiler-embeddable-%{version}
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s license/LICENSE.txt
test -s tree/.archived
test -s tree/.rewritten-b32c9343e34fea6f
test -s tools/compile_modules.py
test -s tools/assemble_embeddable.py
test -s tools/rewrite_kt.py
test -s vendor/vavr/io/vavr/Tuple2.java
test -s vendor/vavr/io/vavr/match/annotation/Patterns.java
test -s vendor/kci/core/commonMain/src/ImmutableCollection.kt
test -s vendor/protobuf-src/formats/protobuf/commonMain/src/kotlinx/serialization/protobuf/ProtoBuf.kt
test -s vendor/cri-impl-src/compiler/build-tools/kotlin-build-tools-cri-impl/src/main/kotlin/org/jetbrains/kotlin/buildtools/internal/cri/CriDataSerializerImpl.kt
test -s vendor/kotlin-annotations-jvm/kotlin/annotations/jvm/ReadOnly.java
test "$(wc -l < modules.txt | tr -d ' ')" -eq 121
test "$(wc -l < project-dirs.tsv | tr -d ' ')" -eq 121

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
export KCE_ROOT="$PWD"
export KCE_OUT="$PWD/kotlin-compiler-embeddable-%{version}.jar"
export KCE_STDLIB=%{_javadir}/kotlin-stdlib-%{version}.jar
export KCE_REFLECT=%{_javadir}/kotlin-reflect-%{version}.jar
export KCE_SCRIPT_RUNTIME=%{_javadir}/kotlin-script-runtime-%{version}.jar
export KCE_COROUTINES=%{_javadir}/kotlinx-coroutines-core-jvm-1.10.2.jar
export KCE_ANNO=/usr/share/kotlin/lib/annotations-13.0.jar
export KCE_ANNO_API=%{_javadir}/org.jetbrains.annotations-24.0.1.jar
export KCE_TROVE=/usr/share/kotlin/lib/trove4j.jar
export KCE_COMPILER_JAR=/usr/share/kotlin/lib/kotlin-compiler.jar
export KCE_GSON=%{_javadir}/gson.jar
export KCE_BTA_API=%{_javadir}/kotlin-build-tools-api.jar
export KCE_GUAVA=%{_javadir}/guava.jar
export KCE_JSR305=%{_javadir}/javax.annotation.jar
export KCE_ANTLR=%{_javadir}/antlr4-runtime.jar
export KCE_SERIAL_CORE=%{_javadir}/kotlinx-serialization-core.jar
export KCE_SERIAL_PLUGIN=/usr/share/kotlin/lib/kotlinx-serialization-compiler-plugin.jar
python tools/compile_modules.py
python tools/assemble_embeddable.py
test -s "$KCE_OUT"

cat > kotlin-compiler-embeddable.pom << END
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.jetbrains.kotlin</groupId>
  <artifactId>kotlin-compiler-embeddable</artifactId>
  <version>%{version}</version>
  <name>kotlin-compiler-embeddable</name>
  <description>Kotlin compiler embeddable.</description>
  <url>https://github.com/JetBrains/kotlin</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-stdlib</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-reflect</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-script-runtime</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlinx</groupId>
      <artifactId>kotlinx-coroutines-core-jvm</artifactId>
      <version>1.10.2</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlinx</groupId>
      <artifactId>atomicfu-jvm</artifactId>
      <version>0.26.1</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.intellij.deps</groupId>
      <artifactId>trove4j</artifactId>
      <version>1.0.20200330</version>
    </dependency>
  </dependencies>
</project>
END

%install
set -eo pipefail
mkdir -p %{buildroot}
sysjar install --buildroot %{buildroot} \
	--artifact kotlin-compiler-embeddable.pom:kotlin-compiler-embeddable-%{version}.jar \
	--file-name kotlin-compiler-embeddable-%{version} \
	--filelist .mfiles
idx="%{buildroot}/usr/share/sysjar/index/org.jetbrains.kotlin/kotlin-compiler-embeddable.sysjar"
moved="%{buildroot}/usr/share/sysjar/index/org.jetbrains.kotlin/kotlin-compiler-embeddable-%{version}.sysjar"
test -s "$idx"
grep -F -q '"version": "%{version}"' "$idx"
grep -F -q '"artifactId": "kotlin-compiler-embeddable"' "$idx"
/bin/mv "$idx" "$moved"
cat > .mfiles << EOF
%%dir /usr/share/sysjar/index/org.jetbrains.kotlin
/usr/share/sysjar/index/org.jetbrains.kotlin/kotlin-compiler-embeddable-%{version}.sysjar
%{_javadir}/kotlin-compiler-embeddable-%{version}.jar
/usr/share/maven-poms/kotlin-compiler-embeddable-%{version}.pom
EOF
test -s %{buildroot}%{_javadir}/kotlin-compiler-embeddable-%{version}.jar
if [ -e %{buildroot}%{_javadir}/kotlin-compiler-embeddable.jar ]; then
	exit 1
fi

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
JAR=%{buildroot}%{_javadir}/kotlin-compiler-embeddable-%{version}.jar
STDLIB=%{_javadir}/kotlin-stdlib-%{version}.jar
REFLECT=%{_javadir}/kotlin-reflect-%{version}.jar
RUNTIME=%{_javadir}/kotlin-script-runtime-%{version}.jar
ANNO=/usr/share/kotlin/lib/annotations-13.0.jar
CO=%{_javadir}/kotlinx-coroutines-core-jvm-1.10.2.jar
ATOMIC=%{_javadir}/atomicfu-jvm.jar
TROVE=/usr/share/kotlin/lib/trove4j.jar
test -s "$JAR"
test -s "$STDLIB"
test -s "$REFLECT"
test -s "$RUNTIME"
test -s "$ANNO"
test -s "$CO"
test -s "$ATOMIC"
test -s "$TROVE"
mkdir -p check/khome/lib check/out
ln -s "$STDLIB" check/khome/lib/kotlin-stdlib.jar
ln -s "$REFLECT" check/khome/lib/kotlin-reflect.jar
ln -s "$RUNTIME" check/khome/lib/kotlin-script-runtime.jar
cat > check/Hello.kt << 'EOF'
fun main() {
    println(40 + 2)
}
EOF
CP="$JAR:$STDLIB:$REFLECT:$RUNTIME:$ANNO:$CO:$ATOMIC:$TROVE"
java -Xmx2g -cp "$CP" org.jetbrains.kotlin.cli.jvm.K2JVMCompiler \
	-kotlin-home check/khome -jvm-target 1.8 -d check/out check/Hello.kt
java -cp "check/out:$STDLIB" HelloKt > check/out.txt
cat check/out.txt
grep -F -qx '42' check/out.txt
echo kotlin_compiler_embeddable_ok 42

%files -f .mfiles
%license license/LICENSE.txt license/vavr-LICENSE license/kci-LICENSE.txt license/kotlinx-serialization-LICENSE.txt
%doc license/NOTICE.txt
